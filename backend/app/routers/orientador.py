from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, or_
from sqlalchemy.orm import selectinload
from datetime import datetime, date
from app.database import get_db
from app.schemas.orientador import EstudianteListItem, CursoDisponible, CursoAsignado
from app.schemas.reporte import ReporteOut
from app.routers.reporte import build_reporte_out
from app.models import Orientador, Estudiante, Evaluacion, ProcesoBPM, Curso, Usuario
from app.utils.dependencies import require_orientador

router = APIRouter(prefix="/orientador", tags=["Panel del Orientador"])

@router.get("/cursos/sin-asignar", response_model=list[CursoDisponible])
async def get_cursos_sin_asignar(orientador: Orientador = Depends(require_orientador), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Curso.id, Curso.nombre, func.count(Estudiante.id).label("total_estudiantes"))
        .outerjoin(Estudiante, Estudiante.curso_id == Curso.id)
        .where(Curso.establecimiento == orientador.establecimiento, Curso.orientador_id.is_(None))
        .group_by(Curso.id, Curso.nombre).order_by(Curso.nombre, Curso.id)
    )
    return [CursoDisponible(id=row.id, nombre=row.nombre, total_estudiantes=row.total_estudiantes)
            for row in result]


@router.post("/cursos/{curso_id}/asignar", response_model=CursoAsignado)
async def asignar_curso(curso_id: int = Path(gt=0), orientador: Orientador = Depends(require_orientador), db: AsyncSession = Depends(get_db)):
    # La condición se comprueba al escribir, incluso ante solicitudes simultáneas.
    # Repetir la asignación propia es seguro; nunca se reemplaza a otro orientador.
    result = await db.execute(
        update(Curso).where(
            Curso.id == curso_id,
            Curso.establecimiento == orientador.establecimiento,
            or_(Curso.orientador_id.is_(None), Curso.orientador_id == orientador.id),
        ).values(orientador_id=orientador.id).execution_options(synchronize_session=False)
    )
    if result.rowcount == 0:
        exists = await db.scalar(select(Curso.id).where(
            Curso.id == curso_id, Curso.establecimiento == orientador.establecimiento))
        await db.rollback()
        if exists is None:
            raise HTTPException(status_code=404, detail="Curso no encontrado en tu establecimiento")
        raise HTTPException(status_code=409, detail="El curso ya tiene otro orientador asignado. Actualiza la lista.")
    await db.commit()
    return CursoAsignado(id=curso_id, orientador_id=orientador.id)


def format_date_spanish(dt) -> str:
    if not dt:
        return "Desconocido"
    today = date.today()
    dt_date = dt.date() if isinstance(dt, datetime) else dt
    if dt_date == today:
        return f"Hoy, {dt.strftime('%I:%M %p')}" if isinstance(dt, datetime) else "Hoy"
    elif (today - dt_date).days == 1:
        return f"Ayer, {dt.strftime('%I:%M %p')}" if isinstance(dt, datetime) else "Ayer"
    else:
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        mes_idx = dt_date.month - 1
        return f"{dt_date.day} de {meses[mes_idx]}, {dt_date.year}"

@router.get("/estudiantes", response_model=list[EstudianteListItem])
async def get_estudiantes(orientador: Orientador = Depends(require_orientador), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Estudiante).join(Curso).where(Curso.orientador_id == orientador.id)
        .options(
            selectinload(Estudiante.usuario),
            selectinload(Estudiante.curso),
            selectinload(Estudiante.evaluaciones).selectinload(Evaluacion.proceso_bpm),
            selectinload(Estudiante.evaluaciones).selectinload(Evaluacion.reporte)
        )
    )
    estudiantes = result.scalars().unique().all()
    
    items = []
    for est in estudiantes:
        evaluacion = est.evaluaciones[-1] if est.evaluaciones else None
        
        dt = evaluacion.created_at if evaluacion else None

        items.append(EstudianteListItem(
            id=est.id,
            name=est.nombre_completo,
            email=est.usuario.email if est.usuario else "Sin email",
            course=est.curso.nombre if est.curso else "Sin curso",
            lastUpdate=format_date_spanish(dt),
            bpm_estado=evaluacion.proceso_bpm.estado_actual if (evaluacion and evaluacion.proceso_bpm) else None,
            estado_evaluacion=evaluacion.estado if evaluacion else None,
            hasReport=bool(evaluacion and evaluacion.reporte)
        ))
        
    return items

@router.get("/estudiante/{estudiante_id}/reporte", response_model=ReporteOut)
async def get_estudiante_reporte(estudiante_id: int, orientador: Orientador = Depends(require_orientador), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Estudiante).join(Curso).where(Estudiante.id == estudiante_id, Curso.orientador_id == orientador.id)
        .options(selectinload(Estudiante.evaluaciones).selectinload(Evaluacion.reporte),
                 selectinload(Estudiante.evaluaciones).selectinload(Evaluacion.proceso_bpm))
    )
    est = result.scalar_one_or_none()
    if not est:
        raise HTTPException(status_code=403, detail="Estudiante no pertenece a este orientador")
        
    evaluacion = est.evaluaciones[-1] if est.evaluaciones else None
    if not evaluacion or not evaluacion.reporte:
        raise HTTPException(status_code=404, detail="No hay reporte para este estudiante")
        
    reporte = evaluacion.reporte[0] if isinstance(evaluacion.reporte, list) else evaluacion.reporte
    return build_reporte_out(reporte, est.nombre_completo,
                             evaluacion.proceso_bpm.estado_actual if evaluacion.proceso_bpm else None)
