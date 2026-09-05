from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.schemas.reporte import ReporteOut, DimensionScore, CareerArea
from app.models import ReporteVocacional, Evaluacion, Estudiante, Usuario
from app.utils.dependencies import require_estudiante, get_current_user
from datetime import datetime

router = APIRouter(prefix="/evaluacion", tags=["Reporte Vocacional"])

DIMENSION_INTERPRETATIONS = {
    "O": "Creativity, curiosity, openness to new experiences",
    "C": "Organization, self-discipline, achievement orientation",
    "E": "Sociability, assertiveness, energy level",
    "A": "Empathy, cooperation, trust",
    "N": "Emotional management, stress handling, stability"
}

DIMENSION_NAMES = {
    "O": "Apertura a la Experiencia",
    "C": "Responsabilidad",
    "E": "Extraversión",
    "A": "Amabilidad",
    "N": "Neuroticismo"
}

DIMENSION_COLORS = {
    "O": "#4F46E5",
    "C": "#10B981",
    "E": "#F59E0B",
    "A": "#EC4899",
    "N": "#EF4444"
}

CAREER_MATRIX = {
    ("O", "C"): CareerArea(title="Tecnología e Informática", desc="Ideal para desarrollo de software y análisis de datos.", carreras=["Ingeniería Informática", "Ciencia de Datos", "Ciberseguridad"]),
    ("C", "O"): CareerArea(title="Ingeniería y Gestión de Procesos", desc="Ideal para planificación y optimización de recursos.", carreras=["Ingeniería Civil Industrial", "Gestión de Proyectos"]),
    ("E", "A"): CareerArea(title="Comunicación y Relaciones Públicas", desc="Enfocado en el manejo de imagen pública y medios.", carreras=["Periodismo", "Relaciones Públicas"]),
    ("A", "E"): CareerArea(title="Salud y Educación", desc="Vocación de servicio, cuidado y enseñanza.", carreras=["Medicina", "Enfermería", "Pedagogía", "Psicología"]),
    ("O", "E"): CareerArea(title="Artes y Diseño", desc="Expresión creativa, comunicación visual y estética.", carreras=["Diseño Gráfico", "Arquitectura", "Artes Visuales"]),
    ("C", "A"): CareerArea(title="Administración y Contabilidad", desc="Manejo ordenado y ético de finanzas y recursos.", carreras=["Contabilidad", "Auditoría", "Administración de Empresas"])
}

def get_career_areas(scores: dict) -> list[CareerArea]:
    # Get top 2 dimensions
    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_dims) >= 2:
        top1, top2 = sorted_dims[0][0], sorted_dims[1][0]
        # Check permutations
        if (top1, top2) in CAREER_MATRIX:
            return [CAREER_MATRIX[(top1, top2)]]
        elif (top2, top1) in CAREER_MATRIX:
            return [CAREER_MATRIX[(top2, top1)]]
    
    # Default if no match
    return [CAREER_MATRIX[("O", "C")]]

def build_reporte_out(reporte: ReporteVocacional) -> ReporteOut:
    scores = reporte.scores_json
    dimensions = []
    for k, v in scores.items():
        dimensions.append(DimensionScore(
            letter=k,
            name=DIMENSION_NAMES.get(k, k),
            score=int(v * 100),
            color=DIMENSION_COLORS.get(k, "#000000"),
            interpretation=DIMENSION_INTERPRETATIONS.get(k, ""),
            vocationalImpact="Alto impacto en áreas relacionadas"
        ))
        
    career_areas = get_career_areas(scores)
    
    # Just format date roughly
    dt_str = "Hoy" if not reporte.created_at else reporte.created_at.strftime("%d de %b, %Y")
    
    return ReporteOut(
        evaluatedAt=dt_str,
        scores=scores,
        dimensions=dimensions,
        careerAreas=career_areas
    )

@router.get("/reporte", response_model=ReporteOut)
async def get_my_report(estudiante: Estudiante = Depends(require_estudiante), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Evaluacion).options(selectinload(Evaluacion.reporte)).where(Evaluacion.estudiante_id == estudiante.id).order_by(Evaluacion.id.desc())
    )
    evaluacion = result.scalars().first()
    if not evaluacion or not evaluacion.reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    rep = evaluacion.reporte[0] if isinstance(evaluacion.reporte, list) else evaluacion.reporte
    return build_reporte_out(rep)

@router.get("/reporte/{reporte_id}", response_model=ReporteOut)
async def get_report_by_id(reporte_id: int, current_user: Usuario = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ReporteVocacional).where(ReporteVocacional.id == reporte_id))
    reporte = result.scalar_one_or_none()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    return build_reporte_out(reporte)
