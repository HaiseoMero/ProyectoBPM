import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class EstadoEvaluacion(str, enum.Enum):
    en_progreso = "en_progreso"
    completada = "completada"
    procesada = "procesada"

class Evaluacion(Base):
    __tablename__ = "evaluacion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    estudiante_id: Mapped[int] = mapped_column(ForeignKey("estudiante.id"), nullable=False)
    estado: Mapped[EstadoEvaluacion] = mapped_column(Enum(EstadoEvaluacion), default=EstadoEvaluacion.en_progreso)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)

    estudiante: Mapped["Estudiante"] = relationship("Estudiante", back_populates="evaluaciones")
    respuestas: Mapped[list["Respuesta"]] = relationship("Respuesta", back_populates="evaluacion", cascade="all, delete-orphan")
    reporte: Mapped["ReporteVocacional"] = relationship("ReporteVocacional", back_populates="evaluacion", uselist=False)
    proceso_bpm: Mapped["ProcesoBPM"] = relationship("ProcesoBPM", back_populates="evaluacion", uselist=False)
