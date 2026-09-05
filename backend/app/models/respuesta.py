from datetime import datetime
from sqlalchemy import ForeignKey, Integer, DateTime, func, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Respuesta(Base):
    __tablename__ = "respuesta"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    evaluacion_id: Mapped[int] = mapped_column(ForeignKey("evaluacion.id"), nullable=False)
    pregunta_id: Mapped[int] = mapped_column(ForeignKey("pregunta.id"), nullable=False)
    valor: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("valor >= 1 AND valor <= 5", name="check_valor_rango"),
        UniqueConstraint("evaluacion_id", "pregunta_id", name="uq_evaluacion_pregunta"),
    )

    evaluacion: Mapped["Evaluacion"] = relationship("Evaluacion", back_populates="respuestas")
    pregunta: Mapped["Pregunta"] = relationship("Pregunta")
