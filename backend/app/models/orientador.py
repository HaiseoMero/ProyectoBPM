from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Orientador(Base):
    __tablename__ = "orientador"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), unique=True, nullable=False)
    nombre_completo: Mapped[str] = mapped_column(String(255), nullable=False)
    departamento: Mapped[str | None] = mapped_column(String(255))

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="orientador")
    cursos: Mapped[list["Curso"]] = relationship("Curso", back_populates="orientador")
