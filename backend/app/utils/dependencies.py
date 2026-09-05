from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError

from app.database import get_db
from app.utils.security import decode_access_token
from app.models.usuario import Usuario

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> Usuario:
    try:
        payload = decode_access_token(credentials.credentials)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    stmt = select(Usuario).where(Usuario.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
        
    return user

async def require_estudiante(user: Usuario = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.rol.value != 'estudiante':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso exclusivo para estudiantes")
    from app.models.estudiante import Estudiante
    result = await db.execute(select(Estudiante).where(Estudiante.usuario_id == user.id))
    estudiante = result.scalar_one_or_none()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Perfil de estudiante no encontrado")
    return estudiante

async def require_orientador(user: Usuario = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.rol.value != 'orientador':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso exclusivo para orientadores")
    from app.models.orientador import Orientador
    result = await db.execute(select(Orientador).where(Orientador.usuario_id == user.id))
    orientador = result.scalar_one_or_none()
    if not orientador:
        raise HTTPException(status_code=404, detail="Perfil de orientador no encontrado")
    return orientador
