"""Servicio de integración con Camunda 8 / Zeebe."""
import os
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.proceso_bpm import ProcesoBPM
from pyzeebe import ZeebeClient, create_insecure_channel
from pyzeebe.errors import ProcessDefinitionNotFoundError

# Configure Zeebe connection
ZEEBE_ADDRESS = os.getenv("ZEEBE_ADDRESS", "zeebe:26500")

_client = None

def get_zeebe_client() -> ZeebeClient:
    global _client
    if _client is None:
        channel = create_insecure_channel(grpc_address=ZEEBE_ADDRESS)
        _client = ZeebeClient(channel)
    return _client

async def start_process(db: AsyncSession, evaluacion_id: int) -> ProcesoBPM:
    """Start Camunda process instance."""
    client = get_zeebe_client()
    
    # Save the initial tracking record
    proceso = ProcesoBPM(evaluacion_id=evaluacion_id, estado_actual="registro")
    db.add(proceso)
    await db.flush()
    
    try:
        # Start the process in Zeebe
        process_instance_key = await client.run_process(
            bpmn_process_id="evaluacion-vocacional",
            variables={"evaluacion_id": evaluacion_id}
        )
        proceso.zeebe_process_instance_key = str(process_instance_key)
        await db.commit()
    except Exception as e:
        print(f"Failed to start Zeebe process: {e}")
        
    return proceso

async def advance_to(db: AsyncSession, proceso: ProcesoBPM, estado: str) -> None:
    """Update BPM state."""
    proceso.estado_actual = estado
    await db.commit()

async def finish_cuestionario(db: AsyncSession, evaluacion_id: int) -> None:
    """Publish message to Zeebe to indicate questionnaire is complete."""
    client = get_zeebe_client()
    try:
        await client.publish_message(
            name="CuestionarioCompletado",
            correlation_key=str(evaluacion_id),
            variables={"evaluacion_id": evaluacion_id}
        )
    except Exception as e:
        print(f"Failed to publish message to Zeebe: {e}")

