from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Estudiante(Base):
    __tablename__ = "estudiante"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), unique=True, nullable=False)
    nombre_completo: Mapped[str] = mapped_column(String(255), nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)
    curso_id: Mapped[int | None] = mapped_column(ForeignKey("curso.id"))

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="estudiante")
    curso: Mapped["Curso"] = relationship("Curso", back_populates="estudiantes")
    evaluaciones: Mapped[list["Evaluacion"]] = relationship("Evaluacion", back_populates="estudiante")
