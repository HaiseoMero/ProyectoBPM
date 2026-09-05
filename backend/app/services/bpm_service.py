"""Servicio de integración con Camunda 8 / Zeebe.

TODO Fase 3: Conectar con camunda-orchestration-sdk o pyzeebe.
Por ahora, actualiza el estado en la tabla proceso_bpm directamente.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.proceso_bpm import ProcesoBPM

async def start_process(db: AsyncSession, evaluacion_id: int) -> ProcesoBPM:
    """Create a BPM tracking record. TODO: Start Camunda process instance."""
    proceso = ProcesoBPM(evaluacion_id=evaluacion_id, estado_actual="registro")
    db.add(proceso)
    await db.flush()
    return proceso

async def advance_to(db: AsyncSession, proceso: ProcesoBPM, estado: str) -> None:
    """Update BPM state. TODO: Complete Camunda user/service task."""
    proceso.estado_actual = estado
    await db.flush()
