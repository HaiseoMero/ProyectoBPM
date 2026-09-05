import enum
from sqlalchemy import String, Integer, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class DimensionEnum(str, enum.Enum):
    O = "O"
    C = "C"
    E = "E"
    A = "A"
    N = "N"

class Pregunta(Base):
    __tablename__ = "pregunta"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    texto: Mapped[str] = mapped_column(String(500), nullable=False)
    dimension: Mapped[DimensionEnum] = mapped_column(Enum(DimensionEnum), nullable=False)
    es_invertida: Mapped[bool] = mapped_column(Boolean, default=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
