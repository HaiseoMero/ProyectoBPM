from app.config import settings
import asyncio
from sqlalchemy import select
from app.database import async_session_maker
from app.models import Evaluacion, ReporteVocacional
from app.models.proceso_bpm import ProcesoBPM
from pyzeebe import Job, ZeebeWorker, create_insecure_channel
from app.services.bpm_service import advance_to, log_event

async def calcular_ocean(evaluacion_id: str, job: Job):
    """Worker for Calcular Puntajes OCEAN."""
    eval_id = int(evaluacion_id)
    async with async_session_maker() as db:
        proceso = (await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == eval_id))).scalar_one_or_none()
        if proceso is None:
            raise ValueError("Proceso BPM no registrado")
        await advance_to(db, proceso, "calculando_ocean", job.process_instance_key)
            
        # The actual scoring is already done by API when submitting the 44 answers, 
        # so this is just for BPM tracking in this architecture.
        # But if we want, we could generate the report here instead of API.
        pass
        
    return {"status": "ocean_calculado"}

async def generar_reporte(evaluacion_id: str, job: Job):
    """Worker for Generar Reporte Vocacional."""
    eval_id = int(evaluacion_id)
    async with async_session_maker() as db:
        proceso = (await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == eval_id))).scalar_one_or_none()
        if proceso is None:
            raise ValueError("Proceso BPM no registrado")
        await advance_to(db, proceso, "generando_reporte", job.process_instance_key)
    return {"status": "reporte_generado"}

async def notificar_orientador(evaluacion_id: str, job: Job):
    """Worker for Notificar Orientador."""
    eval_id = int(evaluacion_id)
    async with async_session_maker() as db:
        proceso = (await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == eval_id))).scalar_one_or_none()
        if proceso is None:
            raise ValueError("Proceso BPM no registrado")
        await advance_to(db, proceso, "reporte_listo", job.process_instance_key)
    return {"status": "notificado"}

async def start_worker():
    """Crear canal y worker dentro del loop que ejecuta la aplicación."""
    channel = create_insecure_channel(grpc_address=settings.ZEEBE_GATEWAY)
    try:
        worker = ZeebeWorker(channel, max_connection_retries=-1)
        worker.task(task_type="calcular-ocean")(calcular_ocean)
        worker.task(task_type="generar-reporte")(generar_reporte)
        worker.task(task_type="notificar-orientador")(notificar_orientador)
        log_event("bpm_worker_starting")
        await worker.work()
    finally:
        await channel.close()
        log_event("bpm_worker_stopped")

if __name__ == "__main__":
    asyncio.run(start_worker())
