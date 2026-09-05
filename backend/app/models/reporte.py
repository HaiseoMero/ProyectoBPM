from datetime import datetime
from sqlalchemy import ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class ReporteVocacional(Base):
    __tablename__ = "reporte_vocacional"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    evaluacion_id: Mapped[int] = mapped_column(ForeignKey("evaluacion.id"), unique=True, nullable=False)
    scores_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    carreras_json: Mapped[list | None] = mapped_column(JSON)
    interpretaciones_json: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    evaluacion: Mapped["Evaluacion"] = relationship("Evaluacion", back_populates="reporte")
