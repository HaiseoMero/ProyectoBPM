from app.config import settings
import asyncio
from sqlalchemy import select
from app.database import async_session_maker
from app.models import Evaluacion, ReporteVocacional
from app.models.proceso_bpm import ProcesoBPM
from pyzeebe import Job, ZeebeWorker, create_insecure_channel
from app.services.bpm_service import advance_to, log_event

channel = create_insecure_channel(grpc_address=settings.ZEEBE_GATEWAY)
worker = ZeebeWorker(channel)

@worker.task(task_type="calcular-ocean")
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

@worker.task(task_type="generar-reporte")
async def generar_reporte(evaluacion_id: str, job: Job):
    """Worker for Generar Reporte Vocacional."""
    eval_id = int(evaluacion_id)
    async with async_session_maker() as db:
        proceso = (await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == eval_id))).scalar_one_or_none()
        if proceso is None:
            raise ValueError("Proceso BPM no registrado")
        await advance_to(db, proceso, "generando_reporte", job.process_instance_key)
    return {"status": "reporte_generado"}

@worker.task(task_type="notificar-orientador")
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
    """Start the Zeebe worker."""
    log_event("bpm_worker_starting")
    await worker.work()

if __name__ == "__main__":
    asyncio.run(start_worker())
