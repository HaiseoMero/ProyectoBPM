from pydantic import BaseModel
from app.models.evaluacion import EstadoEvaluacion

class CursoDisponible(BaseModel):
    id: int
    nombre: str
    total_estudiantes: int


class CursoAsignado(BaseModel):
    id: int
    orientador_id: int


class EstudianteListItem(BaseModel):
    id: int
    name: str
    email: str
    course: str
    lastUpdate: str  # Fecha de inicio de la evaluación; nombre conservado para el consumidor actual.
    bpm_estado: str | None = None
    estado_evaluacion: EstadoEvaluacion | None = None
    hasReport: bool
