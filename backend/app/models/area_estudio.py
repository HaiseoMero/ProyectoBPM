from sqlalchemy import String, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class AreaEstudio(Base):
    __tablename__ = "area_estudio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    area_sies: Mapped[str] = mapped_column(String(80), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(600), nullable=False, default="")
    ideal_o: Mapped[float] = mapped_column(Float, nullable=False)
    ideal_c: Mapped[float] = mapped_column(Float, nullable=False)
    ideal_e: Mapped[float] = mapped_column(Float, nullable=False)
    ideal_a: Mapped[float] = mapped_column(Float, nullable=False)
    ideal_n: Mapped[float] = mapped_column(Float, nullable=False)
    peso_o: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    peso_c: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    peso_e: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    peso_a: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    peso_n: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    carreras_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
