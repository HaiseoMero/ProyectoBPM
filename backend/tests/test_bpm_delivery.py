import asyncio
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from pyzeebe.errors import MessageAlreadyExistsError
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BPMEvento, ProcesoBPM, ReporteVocacional, Evaluacion
from app.services import bpm_service as bpm
from tests.test_evaluacion_respuestas import api, auth, final_payload  # Fixtures HTTP existentes.


@pytest_asyncio.fixture
async def delivery(api, monkeypatch):
    client, sessions = api
    async with sessions() as db:
        db.add(ProcesoBPM(evaluacion_id=1, process_instance_key='123', estado_actual='registro'))
        await db.commit()
    zeebe = SimpleNamespace(topology=AsyncMock(), publish_message=AsyncMock(),
                            run_process=AsyncMock(return_value=SimpleNamespace(process_instance_key=456)))
    monkeypatch.setattr(bpm, 'get_zeebe_client', lambda: zeebe)
    return client, sessions, zeebe


async def ready(sessions):
    async with sessions() as db:
        event = await db.scalar(select(BPMEvento).where(BPMEvento.tipo == 'completar'))
        event.proximo_intento = None
        event_id = event.id
        await db.commit()
    return event_id


@pytest.mark.asyncio
async def test_commit_visible_before_publication_and_repeated_request(delivery):
    client, sessions, zeebe = delivery
    async def publish(**kwargs):
        async with sessions() as db:
            assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 1
            assert (await db.get(Evaluacion, 1)).estado == 'completada'
            assert (await db.scalar(select(BPMEvento))).message_id == kwargs['message_id']
    zeebe.publish_message.side_effect = publish
    result = await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
    assert result.status_code == 200
    assert (await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())).status_code == 400
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(BPMEvento)) == 1
        await bpm.finish_cuestionario(db, 1)
    zeebe.publish_message.assert_awaited_once()


@pytest.mark.asyncio
async def test_failed_report_commit_never_calls_zeebe(delivery, monkeypatch):
    client, sessions, zeebe = delivery
    async def fail(db):
        await db.flush()
        raise RuntimeError('commit failed')
    monkeypatch.setattr(AsyncSession, 'commit', fail)
    with pytest.raises(RuntimeError):
        await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
    zeebe.publish_message.assert_not_awaited()
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(BPMEvento)) == 0
        assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 0


@pytest.mark.asyncio
async def test_zeebe_offline_keeps_report_and_durable_pending_then_recovers(delivery):
    client, sessions, zeebe = delivery
    zeebe.topology.side_effect = ConnectionError('offline')
    response = await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
    assert response.status_code == 200
    zeebe.publish_message.assert_not_awaited()
    async with sessions() as db:
        event = await db.scalar(select(BPMEvento))
        assert event.estado == 'pendiente' and event.ultimo_error == 'ConnectionError'
        assert event.primer_intento is None
        assert await db.get(ReporteVocacional, response.json()['reportId']) is not None
    zeebe.topology.side_effect = None
    event_id = await ready(sessions)
    # Una sesión nueva representa reanudación tras cerrar la petición/reiniciar el proceso.
    async with sessions() as db:
        await bpm.dispatch_event(db, event_id)
    zeebe.publish_message.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize('duplicate', [False, True])
async def test_failed_publication_reuses_message_id(delivery, duplicate):
    client, sessions, zeebe = delivery
    zeebe.publish_message.side_effect = TimeoutError('lost acknowledgement')
    assert (await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())).status_code == 200
    original = zeebe.publish_message.call_args.kwargs
    zeebe.publish_message.side_effect = MessageAlreadyExistsError() if duplicate else None
    event_id = await ready(sessions)
    async with sessions() as db:
        await bpm.dispatch_event(db, event_id)
    assert zeebe.publish_message.call_args.kwargs == original
    async with sessions() as db:
        assert (await db.get(BPMEvento, event_id)).estado == 'enviado'
        assert await db.scalar(select(func.count()).select_from(ReporteVocacional)) == 1


@pytest.mark.asyncio
async def test_commit_failure_after_remote_acceptance_preserves_retry_identity(delivery, monkeypatch):
    client, sessions, zeebe = delivery
    commit = AsyncSession.commit
    async def fail_ack(db):
        if any(isinstance(obj, BPMEvento) and obj.estado == 'enviado' for obj in db.dirty):
            raise RuntimeError('ack commit failed')
        await commit(db)
    monkeypatch.setattr(AsyncSession, 'commit', fail_ack)
    assert (await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())).status_code == 200
    async with sessions() as db:
        event = await db.scalar(select(BPMEvento))
        assert event.estado == 'pendiente' and event.primer_intento is not None
    first_id = zeebe.publish_message.call_args.kwargs['message_id']
    monkeypatch.setattr(AsyncSession, 'commit', commit)
    zeebe.publish_message.side_effect = MessageAlreadyExistsError()
    async with sessions() as db:
        await bpm.finish_cuestionario(db, 1)
    assert zeebe.publish_message.call_args.kwargs['message_id'] == first_id


@pytest.mark.asyncio
async def test_expired_ambiguous_message_requires_review_without_republishing(delivery):
    client, sessions, zeebe = delivery
    zeebe.publish_message.side_effect = TimeoutError()
    await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
    async with sessions() as db:
        event = await db.scalar(select(BPMEvento))
        event.primer_intento = await db.scalar(select(func.now())) - timedelta(days=2)
        event.proximo_intento = None
        event_id = event.id
        await db.commit()
    async with sessions() as db:
        await bpm.dispatch_event(db, event_id)
        assert (await db.get(BPMEvento, event_id)).estado == 'revision'
    zeebe.publish_message.assert_awaited_once()


@pytest.mark.asyncio
async def test_initial_process_has_no_internal_commit_or_rpc(delivery):
    _, sessions, zeebe = delivery
    async with sessions() as db:
        await bpm.start_process(db, 2)
        await db.rollback()
    async with sessions() as db:
        assert await db.scalar(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == 2)) is None
        assert await db.scalar(select(BPMEvento)) is None
    zeebe.run_process.assert_not_awaited()


@pytest.mark.asyncio
async def test_start_offline_then_success_or_uncertain_does_not_duplicate(delivery):
    _, sessions, zeebe = delivery
    async with sessions() as db:
        await bpm.start_process(db, 2)
        await db.commit()
    zeebe.topology.side_effect = ConnectionError()
    async with sessions() as db:
        await bpm.finish_cuestionario(db, 2)
        event = await db.scalar(select(BPMEvento))
        assert event.estado == 'pendiente'
        event.proximo_intento = None
        await db.commit()
    zeebe.topology.side_effect = None
    zeebe.run_process.side_effect = TimeoutError()
    async with sessions() as db:
        await bpm.finish_cuestionario(db, 2)
    async with sessions() as db:
        await bpm.finish_cuestionario(db, 2)
        assert (await db.scalar(select(BPMEvento))).estado == 'incierto'
    zeebe.run_process.assert_awaited_once()


@pytest.mark.asyncio
async def test_sdk_response_instance_key_is_persisted(delivery):
    _, sessions, zeebe = delivery
    async with sessions() as db:
        await bpm.start_process(db, 2)
        await db.commit()
        await bpm.finish_cuestionario(db, 2)
    async with sessions() as db:
        proc = await db.scalar(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == 2))
        assert proc.process_instance_key == '456'
    zeebe.run_process.assert_awaited_once()


@pytest.mark.asyncio
async def test_workers_require_report_and_monotonic_matching_instance(delivery):
    client, sessions, _ = delivery
    async with sessions() as db:
        proc = await db.scalar(select(ProcesoBPM))
        with pytest.raises(ValueError, match='Reporte no confirmado'):
            await bpm.advance_to(db, proc, 'calculando_ocean', 123)
        await db.rollback()
    await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
    async with sessions() as db:
        proc = await db.scalar(select(ProcesoBPM))
        with pytest.raises(ValueError, match='Instancia'):
            await bpm.advance_to(db, proc, 'calculando_ocean', 999)
        with pytest.raises(ValueError, match='fuera de orden'):
            await bpm.advance_to(db, proc, 'reporte_listo', 123)
        for state in ['calculando_ocean', 'generando_reporte', 'reporte_listo', 'calculando_ocean']:
            await bpm.advance_to(db, proc, state, 123)
        assert proc.estado_actual == 'reporte_listo'
        assert (await db.scalar(select(BPMEvento))).estado == 'consumido'


@pytest.mark.asyncio
async def test_periodic_recovery_does_not_require_http_request(delivery, monkeypatch):
    client, sessions, zeebe = delivery
    zeebe.topology.side_effect = ConnectionError()
    await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
    await ready(sessions)
    zeebe.topology.side_effect = None
    monkeypatch.setattr(bpm, 'async_session_maker', sessions)
    delivered = asyncio.Event()
    async def publish(**kwargs):
        delivered.set()
    zeebe.publish_message.side_effect = publish
    task = asyncio.create_task(bpm.retry_pending_events())
    try:
        await asyncio.wait_for(delivered.wait(), 2)
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio
async def test_real_grpc_unavailable_keeps_report_pending(delivery, monkeypatch):
    import socket
    from pyzeebe import ZeebeClient, create_insecure_channel
    client, sessions, _ = delivery
    # Puerto local reservado pero sin listen: no afecta servicios de desarrollo.
    with socket.socket() as unavailable:
        unavailable.bind(('127.0.0.1', 0))
        channel = create_insecure_channel(grpc_address=f'127.0.0.1:{unavailable.getsockname()[1]}')
        monkeypatch.setattr(bpm, 'get_zeebe_client', lambda: ZeebeClient(channel))
        monkeypatch.setattr(bpm, 'RPC_TIMEOUT', 0.5)
        try:
            result = await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
            assert result.status_code == 200
            async with sessions() as db:
                event = await db.scalar(select(BPMEvento))
                assert event.estado == 'pendiente' and event.ultimo_error is not None
                assert event.primer_intento is None
                assert await db.get(ReporteVocacional, result.json()['reportId']) is not None
        finally:
            await channel.close()


@pytest.mark.asyncio
async def test_completion_waits_for_inflight_start_without_becoming_manual(delivery):
    client, sessions, zeebe = delivery
    async with sessions() as db:
        proc = await db.scalar(select(ProcesoBPM))
        proc.process_instance_key = None
        db.add(BPMEvento(evaluacion_id=1, tipo='iniciar', estado='incierto'))
        await db.commit()
    result = await client.post('/api/evaluacion/enviar', headers=auth(1), json=final_payload())
    assert result.status_code == 200
    zeebe.publish_message.assert_not_awaited()
    async with sessions() as db:
        event = await db.scalar(select(BPMEvento).where(BPMEvento.tipo == 'completar'))
        assert event.estado == 'pendiente' and event.ultimo_error == 'esperando_inicio'
        (await db.scalar(select(ProcesoBPM))).process_instance_key = '123'
        await db.commit()
    event_id = await ready(sessions)
    async with sessions() as db:
        await bpm.dispatch_event(db, event_id)
    zeebe.publish_message.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_commit_ack_failure_does_not_recreate_instance(delivery, monkeypatch):
    _, sessions, zeebe = delivery
    async with sessions() as db:
        await bpm.start_process(db, 2)
        await db.commit()
    commit = AsyncSession.commit
    async def fail(db):
        if any(isinstance(obj, BPMEvento) and obj.estado == 'enviado' for obj in db.dirty):
            raise RuntimeError('ack commit failed')
        await commit(db)
    monkeypatch.setattr(AsyncSession, 'commit', fail)
    async with sessions() as db:
        await bpm.finish_cuestionario(db, 2)
    monkeypatch.setattr(AsyncSession, 'commit', commit)
    async with sessions() as db:
        await bpm.finish_cuestionario(db, 2)
        assert (await db.scalar(select(BPMEvento))).estado == 'incierto'
    zeebe.run_process.assert_awaited_once()
