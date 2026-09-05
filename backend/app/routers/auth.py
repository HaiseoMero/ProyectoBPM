from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, UserProfile
from app.models import Usuario, Estudiante, Orientador
from app.utils.security import verify_password, create_access_token, hash_password
from app.utils.dependencies import get_current_user
from app.services.auth_service import create_user, authenticate_user, get_user_name

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    token = create_access_token({"sub": user.email, "role": user.rol.value})
    name = await get_user_name(user, db)
    
    return LoginResponse(access_token=token, role=user.rol.value, name=name)

@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Usuario).where(Usuario.email == request.email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado"
        )
    
    if request.role == "estudiante" and (request.edad is None or request.curso_id is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Edad y curso son requeridos para estudiantes"
        )
        
    await create_user(
        db=db,
        email=request.email,
        password=request.password,
        role=request.role,
        nombre=request.nombre_completo,
        edad=request.edad,
        curso_id=request.curso_id,
        departamento=request.departamento
    )
    
    return RegisterResponse(ok=True, message="Usuario registrado exitosamente")

@router.get("/me", response_model=UserProfile)
async def get_me(current_user: Usuario = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    name = await get_user_name(current_user, db)
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        role=current_user.rol.value,
        name=name
    )
