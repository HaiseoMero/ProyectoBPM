from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Usuario, Estudiante, Orientador, Curso
from app.utils.security import hash_password, verify_password

async def create_user(
    db: AsyncSession, email: str, password: str, role: str, nombre: str,
    nivel: str | None = None, letra: str | None = None, departamento: str | None = None
) -> Usuario:
    hashed_pwd = hash_password(password)
    user = Usuario(email=email, hashed_password=hashed_pwd, rol=role)
    db.add(user)
    await db.flush()
    
    if role == "estudiante":
        curso_nombre = f"{nivel} {letra}"
        result = await db.execute(select(Curso).where(Curso.nombre == curso_nombre))
        curso = result.scalar_one_or_none()
        
        if not curso:
            curso = Curso(nombre=curso_nombre, establecimiento="N/A")
            db.add(curso)
            await db.flush()
            
        estudiante = Estudiante(usuario_id=user.id, nombre_completo=nombre, edad=15, curso_id=curso.id)
        db.add(estudiante)
    elif role == "orientador":
        orientador = Orientador(usuario_id=user.id, nombre_completo=nombre, departamento=departamento)
        db.add(orientador)
        
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_user_name(user: Usuario, db: AsyncSession) -> str:
    if user.rol.value == "estudiante":
        result = await db.execute(select(Estudiante).where(Estudiante.usuario_id == user.id))
        est = result.scalar_one_or_none()
        return est.nombre_completo if est else "Estudiante"
    elif user.rol.value == "orientador":
        result = await db.execute(select(Orientador).where(Orientador.usuario_id == user.id))
        ori = result.scalar_one_or_none()
        return ori.nombre_completo if ori else "Orientador"
    return "Usuario"
