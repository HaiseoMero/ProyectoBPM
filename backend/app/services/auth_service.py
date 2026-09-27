import hmac
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, OperationalError
from app.config import settings
from app.models import Usuario, Estudiante, Orientador, Curso
from app.models.estudiante import calcular_edad
from app.schemas.auth import RegisterRequest
from app.utils.security import hash_password, verify_password


async def create_user(db: AsyncSession, request: RegisterRequest) -> None:
    if request.role == "orientador":
        configured = settings.ORIENTADOR_REGISTRATION_CODE
        secret = configured.get_secret_value() if configured else ""
        if not secret.strip():
            raise HTTPException(403, "El registro de orientadores está deshabilitado")
        supplied = request.codigo_verificacion
        code = supplied.get_secret_value() if supplied else ""
        if not hmac.compare_digest(code.encode(), secret.encode()):
            raise HTTPException(403, "Código de verificación incorrecto")

    hashed_pwd = hash_password(request.password)
    for attempt in range(3):
        try:
            # SERIALIZABLE protege también las búsquedas sin resultados (cero orientadores).
            # Se configura antes de cualquier consulta y solo para esta transacción.
            if db.get_bind().dialect.name == "mysql":
                await db.connection(execution_options={"isolation_level": "SERIALIZABLE"})
            existing = await db.scalar(select(Usuario.id).where(Usuario.email == request.email))
            if existing is not None:
                raise HTTPException(409, "El email ya está registrado")
            user = Usuario(email=request.email, hashed_password=hashed_pwd, rol=request.role)
            db.add(user)
            await db.flush()

            if request.role == "orientador":
                db.add(Orientador(
                    usuario_id=user.id, nombre_completo=request.nombre_completo,
                    departamento=request.departamento, establecimiento=request.establecimiento,
                ))
                await db.flush()

            orientadores = (await db.scalars(
                select(Orientador.id).where(Orientador.establecimiento == request.establecimiento)
                .with_for_update()
            )).all()
            unico = orientadores[0] if len(orientadores) == 1 else None

            if request.role == "estudiante":
                nombre_curso = f"{request.nivel} {request.letra}"
                curso = await db.scalar(select(Curso).where(
                    Curso.establecimiento == request.establecimiento, Curso.nombre == nombre_curso,
                ).with_for_update())
                if curso is None:
                    curso = Curso(nombre=nombre_curso, establecimiento=request.establecimiento)
                    db.add(curso)
                if curso.orientador_id is None and unico is not None:
                    curso.orientador_id = unico
                await db.flush()
                db.add(Estudiante(
                    usuario_id=user.id, nombre_completo=request.nombre_completo,
                    fecha_nacimiento=request.fecha_nacimiento,
                    edad=calcular_edad(request.fecha_nacimiento), curso_id=curso.id,
                ))
            elif unico is not None:
                await db.execute(update(Curso).where(
                    Curso.establecimiento == request.establecimiento,
                    Curso.orientador_id.is_(None),
                ).values(orientador_id=unico))

            await db.commit()
            return
        except (IntegrityError, OperationalError) as exc:
            await db.rollback()
            mysql_code = exc.orig.args[0] if exc.orig.args else None
            retryable = isinstance(exc, IntegrityError) or mysql_code in (1205, 1213)
            if retryable and attempt < 2:
                continue
            if retryable:
                raise HTTPException(409, "Conflicto durante el registro. Intenta nuevamente") from None
            raise HTTPException(503, "No se pudo completar el registro. Intenta nuevamente") from None
        except Exception:
            await db.rollback()
            raise


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
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
