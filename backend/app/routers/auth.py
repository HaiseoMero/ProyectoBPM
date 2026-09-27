from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, UserProfile
from app.models import Usuario
from app.utils.security import create_access_token
from app.utils.dependencies import get_current_user
from app.services.auth_service import create_user, authenticate_user, get_user_name

from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError


class AuthRoute(APIRoute):
    def get_route_handler(self):
        handler = super().get_route_handler()

        async def without_credentials_in_errors(request):
            try:
                return await handler(request)
            except RequestValidationError as exc:
                # Pydantic incluye el input en errores: nunca devolver contraseñas/códigos.
                detail = [{"loc": e["loc"], "msg": e["msg"], "type": e["type"]} for e in exc.errors()]
                raise HTTPException(422, detail=detail) from None

        return without_credentials_in_errors


router = APIRouter(prefix="/auth", tags=["Autenticación"], route_class=AuthRoute)

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
    await create_user(db, request)

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
