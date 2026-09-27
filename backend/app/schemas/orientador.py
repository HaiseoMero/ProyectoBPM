from pydantic import BaseModel

class EstudianteListItem(BaseModel):
    id: int
    name: str
    email: str
    course: str
    lastUpdate: str  # Fecha de inicio de la evaluación; nombre conservado para el consumidor actual.
    bpm_estado: str | None = None
