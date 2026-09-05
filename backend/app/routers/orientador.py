from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, date
from app.database import get_db
from app.schemas.orientador import EstudianteListItem
from app.models import Orientador, Estudiante, Evaluacion, ProcesoBPM, Curso, Usuario
from app.utils.dependencies import require_orientador

router = APIRouter(prefix="/orientador", tags=["Panel del Orientador"])

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
            selectinload(Estudiante.evaluaciones).selectinload(Evaluacion.proceso_bpm)
        )
    )
    estudiantes = result.scalars().unique().all()
    
    items = []
    for est in estudiantes:
        evaluacion = est.evaluaciones[-1] if est.evaluaciones else None
        
        bpm_status_raw = evaluacion.proceso_bpm.estado_actual if (evaluacion and evaluacion.proceso_bpm) else "registro"
        dt = evaluacion.created_at if evaluacion else None
        
        status_map = {
            'reporte_listo': 'success',
            'evaluacion': 'warning',
            'registro': 'info',
            'procesamiento': 'danger'
        }
        
        name_map = {
            'reporte_listo': 'Reporte Listo',
            'evaluacion': 'Evaluación',
            'registro': 'Registro',
            'procesamiento': 'Procesamiento'
        }
        
        items.append(EstudianteListItem(
            id=est.id,
            name=est.nombre_completo,
            email=est.usuario.email if est.usuario else "Sin email",
            course=est.curso.nombre if est.curso else "Sin curso",
            lastUpdate=format_date_spanish(dt),
            bpmStatus=name_map.get(bpm_status_raw, "Registro"),
            statusClass=status_map.get(bpm_status_raw, "info")
        ))
        
    return items

@router.get("/estudiante/{estudiante_id}/reporte")
async def get_estudiante_reporte(estudiante_id: int, orientador: Orientador = Depends(require_orientador), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Estudiante).join(Curso).where(Estudiante.id == estudiante_id, Curso.orientador_id == orientador.id)
        .options(selectinload(Estudiante.evaluaciones).selectinload(Evaluacion.reporte))
    )
    est = result.scalar_one_or_none()
    if not est:
        raise HTTPException(status_code=403, detail="Estudiante no pertenece a este orientador")
        
    evaluacion = est.evaluaciones[-1] if est.evaluaciones else None
    if not evaluacion or not evaluacion.reporte:
        raise HTTPException(status_code=404, detail="No hay reporte para este estudiante")
        
    return evaluacion.reporte[0] if isinstance(evaluacion.reporte, list) else evaluacion.reporte
