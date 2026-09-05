import enum
from datetime import datetime
from sqlalchemy import String, Enum, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class RolEnum(str, enum.Enum):
    estudiante = "estudiante"
    orientador = "orientador"

class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RolEnum] = mapped_column(Enum(RolEnum), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=func.now())

    estudiante: Mapped["Estudiante"] = relationship("Estudiante", back_populates="usuario", uselist=False)
    orientador: Mapped["Orientador"] = relationship("Orientador", back_populates="usuario", uselist=False)
