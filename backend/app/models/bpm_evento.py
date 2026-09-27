"""Bandeja transaccional: entrega técnica separada del estado de negocio BPM."""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class BPMEvento(Base):
    __tablename__ = 'bpm_evento'
    __table_args__ = (UniqueConstraint('evaluacion_id', 'tipo', name='uq_bpm_evento_evaluacion_tipo'),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    evaluacion_id: Mapped[int] = mapped_column(ForeignKey('evaluacion.id'), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    message_id: Mapped[str] = mapped_column(String(36), unique=True, default=lambda: str(uuid4()))
    estado: Mapped[str] = mapped_column(String(20), default='pendiente', nullable=False)
    intentos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    primer_intento: Mapped[datetime | None] = mapped_column(DateTime)
    proximo_intento: Mapped[datetime | None] = mapped_column(DateTime)
    ultimo_error: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
