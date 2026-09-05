import os
import asyncio
from sqlalchemy import select
from app.database import async_session_maker
from app.models import Evaluacion, ReporteVocacional
from app.models.proceso_bpm import ProcesoBPM
from pyzeebe import ZeebeWorker, create_insecure_channel
from app.services.bpm_service import advance_to

ZEEBE_ADDRESS = os.getenv("ZEEBE_ADDRESS", "zeebe:26500")

channel = create_insecure_channel(grpc_address=ZEEBE_ADDRESS)
worker = ZeebeWorker(channel)

@worker.task(task_type="calcular-ocean")
async def calcular_ocean(evaluacion_id: str):
    """Worker for Calcular Puntajes OCEAN."""
    eval_id = int(evaluacion_id)
    async with async_session_maker() as db:
        proceso = (await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == eval_id))).scalar_one_or_none()
        if proceso:
            await advance_to(db, proceso, "calculando_ocean")
            
        # The actual scoring is already done by API when submitting the 44 answers, 
        # so this is just for BPM tracking in this architecture.
        # But if we want, we could generate the report here instead of API.
        pass
        
    return {"status": "ocean_calculado"}

@worker.task(task_type="generar-reporte")
async def generar_reporte(evaluacion_id: str):
    """Worker for Generar Reporte Vocacional."""
    eval_id = int(evaluacion_id)
    async with async_session_maker() as db:
        proceso = (await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == eval_id))).scalar_one_or_none()
        if proceso:
            await advance_to(db, proceso, "generando_reporte")
    return {"status": "reporte_generado"}

@worker.task(task_type="notificar-orientador")
async def notificar_orientador(evaluacion_id: str):
    """Worker for Notificar Orientador."""
    eval_id = int(evaluacion_id)
    async with async_session_maker() as db:
        proceso = (await db.execute(select(ProcesoBPM).where(ProcesoBPM.evaluacion_id == eval_id))).scalar_one_or_none()
        if proceso:
            await advance_to(db, proceso, "reporte_listo")
    return {"status": "notificado"}

async def start_worker():
    """Start the Zeebe worker."""
    print("Starting Zeebe worker...")
    await worker.work()

if __name__ == "__main__":
    asyncio.run(start_worker())
