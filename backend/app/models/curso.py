from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Curso(Base):
    __tablename__ = "curso"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    establecimiento: Mapped[str] = mapped_column(String(255), nullable=False)
    orientador_id: Mapped[int | None] = mapped_column(ForeignKey("orientador.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    orientador: Mapped["Orientador"] = relationship("Orientador", back_populates="cursos")
    estudiantes: Mapped[list["Estudiante"]] = relationship("Estudiante", back_populates="curso")
