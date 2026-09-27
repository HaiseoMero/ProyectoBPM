from datetime import date
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def calcular_edad(nacimiento: date, hoy: date | None = None) -> int:
    hoy = hoy or date.today()
    return hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))


class Estudiante(Base):
    __tablename__ = "estudiante"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), unique=True, nullable=False)
    nombre_completo: Mapped[str] = mapped_column(String(255), nullable=False)
    _edad_historica: Mapped[int] = mapped_column("edad", Integer, nullable=False)
    fecha_nacimiento: Mapped[date | None] = mapped_column(Date, nullable=True)
    curso_id: Mapped[int | None] = mapped_column(ForeignKey("curso.id"))

    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="estudiante")
    curso: Mapped["Curso"] = relationship("Curso", back_populates="estudiantes")
    evaluaciones: Mapped[list["Evaluacion"]] = relationship("Evaluacion", back_populates="estudiante")

    @property
    def edad(self) -> int:
        # La columna existente conserva la edad histórica; con fecha real se calcula al leer.
        return calcular_edad(self.fecha_nacimiento) if self.fecha_nacimiento else self._edad_historica

    @edad.setter
    def edad(self, value: int) -> None:
        self._edad_historica = value
