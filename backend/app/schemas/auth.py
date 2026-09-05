from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class LoginResponse(BaseModel):
    token: str
    role: Literal["estudiante", "orientador"]
    name: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    nombre_completo: str = Field(min_length=2)
    role: Literal["estudiante", "orientador"]
    # Student-specific (optional for orientador)
    edad: int | None = None
    curso_id: int | None = None
    # Orientador-specific
    departamento: str | None = None

class RegisterResponse(BaseModel):
    ok: bool
    message: str

class UserProfile(BaseModel):
    id: int
    email: str
    role: str
    name: str
    model_config = {"from_attributes": True}
