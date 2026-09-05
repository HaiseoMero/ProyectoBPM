from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class ProcesoBPM(Base):
    __tablename__ = "proceso_bpm"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    evaluacion_id: Mapped[int] = mapped_column(ForeignKey("evaluacion.id"), unique=True, nullable=False)
    process_instance_key: Mapped[str | None] = mapped_column(String(100))
    estado_actual: Mapped[str] = mapped_column(String(50), default="registro")
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    evaluacion: Mapped["Evaluacion"] = relationship("Evaluacion", back_populates="proceso_bpm")
