"""Outbox MySQL para Zeebe. No hay transacción distribuida ni exactly-once ilimitado."""
import asyncio
import json
import logging
from datetime import timedelta

from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from pyzeebe import ZeebeClient, create_insecure_channel
from pyzeebe.errors import MessageAlreadyExistsError, ProcessDefinitionNotFoundError

from app.config import settings
from app.database import async_session_maker
from app.models import BPMEvento, Evaluacion, ProcesoBPM, ReporteVocacional

logger = logging.getLogger(__name__)
RPC_TIMEOUT = 5
POLL_SECONDS = 5
MESSAGE_TTL_MS = 24 * 60 * 60 * 1000
# Detener reintentos antes de expirar la retención del primer mensaje posiblemente aceptado.
RETRY_WINDOW = timedelta(hours=23)
STATES = ('registro', 'calculando_ocean', 'generando_reporte', 'reporte_listo')
_client = None


def log_event(event, **fields):
    logger.warning(json.dumps({'event': event, **fields}, ensure_ascii=False))


def get_zeebe_client() -> ZeebeClient:
    global _client
    if _client is None:
        _client = ZeebeClient(create_insecure_channel(grpc_address=settings.ZEEBE_GATEWAY))
    return _client


async def start_process(db: AsyncSession, evaluacion_id: int) -> ProcesoBPM:
    """Preparar inicio junto a la primera respuesta; sin RPC ni commit interno."""
    proceso = ProcesoBPM(evaluacion_id=evaluacion_id, estado_actual='registro')
    db.add(proceso)
    db.add(BPMEvento(evaluacion_id=evaluacion_id, tipo='iniciar'))
    await db.flush()
    return proceso


async def queue_cuestionario(db: AsyncSession, evaluacion_id: int) -> None:
    """Se confirma atómicamente con respuestas, reporte y completed_at."""
    db.add(BPMEvento(evaluacion_id=evaluacion_id, tipo='completar'))


async def _locked_event(db, event_id):
    return await db.scalar(select(BPMEvento).where(BPMEvento.id == event_id)
                           .with_for_update(skip_locked=True).execution_options(populate_existing=True))


async def _retry_later(db, event, now, error):
    event.ultimo_error = error
    event.proximo_intento = now + timedelta(seconds=min(300, 5 * 2 ** min(event.intentos, 6)))
    log_event('bpm_delivery_failed', event_id=event.id, evaluacion_id=event.evaluacion_id,
              tipo=event.tipo, estado=event.estado, error=error)
    await db.commit()


async def dispatch_event(db: AsyncSession, event_id: int) -> None:
    """Bloqueo de fila durante RPC; sesiones competidoras omiten el evento ocupado.

    El primer intento se confirma ANTES del RPC para sobrevivir a una caída tras
    aceptación remota. Un inicio incierto nunca se recrea automáticamente.
    """
    event = await _locked_event(db, event_id)
    now = await db.scalar(select(func.now()))
    if event is None or event.estado not in ('pendiente', 'enviado'):
        await db.rollback()
        return
    if event.estado == 'enviado':
        if event.tipo == 'completar' and event.primer_intento + timedelta(milliseconds=MESSAGE_TTL_MS) < now:
            event.estado = 'revision'
            event.ultimo_error = 'sin_confirmacion_worker'
            log_event('bpm_reconciliation_required', event_id=event.id, error=event.ultimo_error)
            await db.commit()
        else:
            await db.rollback()
        return
    if event.proximo_intento and event.proximo_intento > now:
        await db.rollback()
        return
    proceso = await db.scalar(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == event.evaluacion_id))
    if proceso is None:
        event.estado, event.ultimo_error = 'revision', 'proceso_ausente'
        await db.commit()
        return
    if event.tipo == 'completar':
        report_id = await db.scalar(select(ReporteVocacional.id).where(ReporteVocacional.evaluacion_id == event.evaluacion_id))
        evaluation_state = await db.scalar(select(Evaluacion.estado).where(Evaluacion.id == event.evaluacion_id))
        if not report_id or evaluation_state not in ('completada', 'procesada'):
            event.estado, event.ultimo_error = 'revision', 'reporte_no_confirmado'
            await db.commit()
            return
        if not proceso.process_instance_key:
            start = await db.scalar(select(BPMEvento).where(BPMEvento.evaluacion_id == event.evaluacion_id, BPMEvento.tipo == 'iniciar'))
            if start is None:
                event.estado, event.ultimo_error = 'revision', 'inicio_sin_confirmar'
                await db.commit()
            else:
                # Un inicio incierto puede estar aún en vuelo. Esperar la key sin
                # recrear instancias; si falló, requiere conciliación del inicio.
                event.proximo_intento = now + timedelta(seconds=30)
                event.ultimo_error = 'esperando_inicio'
                await db.commit()
            return
        if event.primer_intento and now - event.primer_intento >= RETRY_WINDOW:
            event.estado, event.ultimo_error = 'revision', 'ventana_reintento_agotada'
            log_event('bpm_reconciliation_required', event_id=event.id, error=event.ultimo_error)
            await db.commit()
            return
    client = get_zeebe_client()
    try:
        # Una caída conocida antes de enviar deja el evento pendiente indefinidamente.
        await asyncio.wait_for(client.topology(), RPC_TIMEOUT)
    except Exception as exc:
        await _retry_later(db, event, now, type(exc).__name__)
        return

    if event.primer_intento is None:
        event.primer_intento = now
    if event.tipo == 'iniciar':
        event.estado = 'incierto'
    event.intentos += 1
    await db.commit()  # Marca durable antes del efecto remoto, nunca commit de la evaluación.
    event = await _locked_event(db, event_id)
    # Otro dispatcher pudo confirmar la publicación entre ambas transacciones.
    if event is None or event.estado not in ('pendiente', 'incierto'):
        await db.rollback()
        return
    if event.proximo_intento and event.proximo_intento > now:
        await db.rollback()
        return
    try:
        if event.tipo == 'iniciar':
            response = await asyncio.wait_for(client.run_process(
                bpmn_process_id='evaluacion-vocacional',
                variables={'evaluacion_id': event.evaluacion_id}), RPC_TIMEOUT)
            key = int(getattr(response, 'process_instance_key', response))
            proceso = await db.scalar(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == event.evaluacion_id))
            proceso.process_instance_key = str(key)
        else:
            try:
                await asyncio.wait_for(client.publish_message(
                    name='CuestionarioCompletado', correlation_key=str(event.evaluacion_id),
                    variables={'evaluacion_id': event.evaluacion_id},
                    message_id=event.message_id, time_to_live_in_milliseconds=MESSAGE_TTL_MS), RPC_TIMEOUT)
            except MessageAlreadyExistsError:
                pass  # Zeebe confirma que ese mismo mensaje ya está retenido.
    except Exception as exc:
        if event.tipo == 'iniciar' and isinstance(exc, ProcessDefinitionNotFoundError):
            event.estado, event.primer_intento = 'pendiente', None  # Rechazo explícito: no creó instancia.
        await _retry_later(db, event, now, type(exc).__name__)
        return
    event.estado, event.ultimo_error, event.proximo_intento = 'enviado', None, None
    await db.commit()


async def finish_cuestionario(db: AsyncSession, evaluacion_id: int) -> None:
    """Entrega después del commit; un fallo posterior nunca invalida el reporte."""
    try:
        ids = (await db.scalars(select(BPMEvento.id).where(
            BPMEvento.evaluacion_id == evaluacion_id).order_by(BPMEvento.id))).all()
        await db.rollback()  # Finalizar la lectura; dispatch usa transacciones independientes.
        for event_id in ids:
            await dispatch_event(db, event_id)
    except Exception as exc:
        await db.rollback()
        log_event('bpm_dispatch_failed', evaluacion_id=evaluacion_id, error=type(exc).__name__)


async def retry_pending_events():
    """Reanudar desde MySQL tras reinicios, sin depender de otra petición HTTP."""
    while True:
        try:
            async with async_session_maker() as db:
                now = await db.scalar(select(func.now()))
                ids = (await db.scalars(select(BPMEvento.id).where(
                    or_(BPMEvento.estado == 'pendiente',
                        (BPMEvento.estado == 'enviado') & (BPMEvento.tipo == 'completar') &
                        (BPMEvento.primer_intento < now - timedelta(milliseconds=MESSAGE_TTL_MS))),
                    or_(BPMEvento.proximo_intento.is_(None), BPMEvento.proximo_intento <= func.now()),
                ).order_by(BPMEvento.id).limit(100))).all()
            for event_id in ids:
                async with async_session_maker() as db:
                    try:
                        await dispatch_event(db, event_id)
                    except Exception as exc:
                        await db.rollback()
                        log_event('bpm_dispatch_failed', event_id=event_id, error=type(exc).__name__)
        except Exception as exc:
            log_event('bpm_retry_loop_failed', error=type(exc).__name__)
        await asyncio.sleep(POLL_SECONDS)


async def advance_to(db: AsyncSession, proceso: ProcesoBPM, estado: str, process_instance_key=None) -> None:
    """Workers idempotentes: no avanzar sin reporte, saltar pasos ni retroceder."""
    event = await db.scalar(select(BPMEvento).where(
        BPMEvento.evaluacion_id == proceso.evaluacion_id, BPMEvento.tipo == 'completar').with_for_update())
    proceso = await db.scalar(select(ProcesoBPM).where(ProcesoBPM.id == proceso.id)
                             .with_for_update().execution_options(populate_existing=True))
    report = await db.scalar(select(ReporteVocacional.id).where(ReporteVocacional.evaluacion_id == proceso.evaluacion_id))
    evaluation_state = await db.scalar(select(Evaluacion.estado).where(Evaluacion.id == proceso.evaluacion_id))
    if not report or evaluation_state not in ('completada', 'procesada'):
        raise ValueError('Reporte no confirmado en MySQL')
    if process_instance_key is not None and str(process_instance_key) != proceso.process_instance_key:
        raise ValueError('Instancia Zeebe no corresponde al proceso registrado')
    current, target = STATES.index(proceso.estado_actual), STATES.index(estado)
    if target > current + 1:
        raise ValueError('Transición BPM fuera de orden')
    if target > current:
        proceso.estado_actual = estado
    if event:
        event.estado, event.ultimo_error = 'consumido', None
    await db.commit()
