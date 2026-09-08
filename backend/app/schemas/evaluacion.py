from pydantic import BaseModel, Field
from typing import Literal

class PreguntaOut(BaseModel):
    id: int
    text: str  # mapped from 'texto'
    dimension: Literal["O", "C", "E", "A", "N"]
    model_config = {"from_attributes": True}

class RespuestaIn(BaseModel):
    preguntaId: int
    valor: int = Field(ge=1, le=5)

class RespuestaOut(BaseModel):
    preguntaId: int
    valor: int
    saved: bool = True

class SubmitEvaluationRequest(BaseModel):
    respuestas: list[RespuestaIn]

class SubmitEvaluationResponse(BaseModel):
    reportId: int
    status: str

from datetime import datetime

class EstadoEvaluacion(BaseModel):
    tiene_evaluacion: bool
    estado: str | None = None  # 'en_progreso', 'completada', 'procesada'
    bpm_estado: str | None = None  # 'registro', 'evaluacion', 'procesamiento', 'reporte_listo'
    registro_fecha: datetime | None = None
    evaluacion_fecha: datetime | None = None
    reporte_fecha: datetime | None = None
    orientador_nombre: str | None = None
