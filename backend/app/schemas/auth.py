from datetime import date
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator, model_validator
from typing import Literal
from app.models.estudiante import calcular_edad

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class LoginResponse(BaseModel):
    access_token: str
    role: Literal["estudiante", "orientador"]
    name: str

class RegisterRequest(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=6)
    nombre_completo: str = Field(min_length=2, max_length=255)
    role: Literal["estudiante", "orientador"]
    establecimiento: str = Field(min_length=1, max_length=255)
    # Student-specific (optional for orientador)
    nivel: Literal["1° Medio", "2° Medio", "3° Medio", "4° Medio"] | None = None
    letra: str | None = Field(default=None, pattern=r"^[A-L]$")
    fecha_nacimiento: date | None = None
    # Orientador-specific
    departamento: str | None = Field(default=None, max_length=255)
    codigo_verificacion: SecretStr | None = None

    @field_validator("nombre_completo", "establecimiento", "departamento", "letra", mode="before")
    @classmethod
    def limpiar_texto(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("fecha_nacimiento", mode="before")
    @classmethod
    def validar_fecha(cls, value):
        if value is None:
            return None
        try:
            # Aceptar únicamente fechas civiles ISO, no timestamps ni horas.
            nacimiento = date.fromisoformat(value) if isinstance(value, str) and len(value) == 10 else None
        except ValueError:
            nacimiento = None
        if nacimiento is None:
            raise ValueError("La fecha de nacimiento debe ser una fecha válida (AAAA-MM-DD)")
        if nacimiento >= date.today() or calcular_edad(nacimiento) > 120:
            raise ValueError("La fecha de nacimiento debe ser pasada y no superar los 120 años")
        return nacimiento

    @model_validator(mode="after")
    def validar_rol(self):
        if self.role == "estudiante":
            if self.nivel is None or self.letra is None or self.fecha_nacimiento is None:
                raise ValueError("Estudiantes: indica nivel, letra y fecha de nacimiento")
            if self.departamento is not None or self.codigo_verificacion is not None:
                raise ValueError("Los campos de orientador no corresponden a un estudiante")
        elif self.nivel is not None or self.letra is not None or self.fecha_nacimiento is not None:
            raise ValueError("Los campos de estudiante no corresponden a un orientador")
        return self

class RegisterResponse(BaseModel):
    ok: bool
    message: str

class UserProfile(BaseModel):
    id: int
    email: str
    role: str
    name: str
    model_config = {"from_attributes": True}
