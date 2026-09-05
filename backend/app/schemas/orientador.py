from pydantic import BaseModel

class EstudianteListItem(BaseModel):
    id: int
    name: str
    email: str
    course: str
    lastUpdate: str
    bpmStatus: str
    statusClass: str  # CSS class: 'success', 'warning', 'info', 'danger'
