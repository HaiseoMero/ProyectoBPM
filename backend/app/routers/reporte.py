from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.schemas.reporte import ReporteOut, DimensionScore, CareerArea
from app.models import ReporteVocacional, Evaluacion, Estudiante, Usuario, Curso, Orientador
from app.utils.dependencies import require_estudiante, get_current_user
from datetime import datetime

router = APIRouter(prefix="/evaluacion", tags=["Reporte Vocacional"])

# Descripciones generales de dimensiones; no inferencias sobre profesiones ni diagnósticos.
DIMENSION_INTERPRETATIONS = {
    "O": "Creatividad, curiosidad y apertura a nuevas experiencias.",
    "C": "Organización, autodisciplina y orientación al logro.",
    "E": "Sociabilidad, asertividad y nivel de energía.",
    "A": "Empatía, cooperación y confianza en los demás.",
    "N": "Tendencia a experimentar preocupación, tensión y emociones desagradables. No indica una inclinación profesional."
}

VOCATIONAL_SCOPE = "Este puntaje por sí solo no permite inferir aptitud ni recomendar una profesión."
AREA_SCOPE = "Referencia exploratoria de las reglas del prototipo; no acredita afinidad ni aptitud profesional."

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

# Asociaciones preexistentes del prototipo: no equivalen a evidencia de ajuste vocacional.
CAREER_MATRIX = {
    ("O", "C"): CareerArea(title="Tecnología e Informática", desc="Incluye desarrollo de software y análisis de datos. " + AREA_SCOPE, carreras=["Ingeniería Informática", "Ciencia de Datos", "Ciberseguridad"]),
    ("C", "O"): CareerArea(title="Ingeniería y Gestión de Procesos", desc="Incluye planificación y gestión de procesos y recursos. " + AREA_SCOPE, carreras=["Ingeniería Civil Industrial", "Gestión de Proyectos"]),
    ("E", "A"): CareerArea(title="Comunicación y Relaciones Públicas", desc="Incluye comunicación, medios y relaciones públicas. " + AREA_SCOPE, carreras=["Periodismo", "Relaciones Públicas"]),
    ("A", "E"): CareerArea(title="Salud y Educación", desc="Incluye atención de salud y enseñanza. " + AREA_SCOPE, carreras=["Medicina", "Enfermería", "Pedagogía", "Psicología"]),
    ("O", "E"): CareerArea(title="Artes y Diseño", desc="Incluye creación artística, comunicación visual y diseño. " + AREA_SCOPE, carreras=["Diseño Gráfico", "Arquitectura", "Artes Visuales"]),
    ("C", "A"): CareerArea(title="Administración y Contabilidad", desc="Incluye administración, contabilidad y auditoría. " + AREA_SCOPE, carreras=["Contabilidad", "Auditoría", "Administración de Empresas"])
}

def get_career_areas(scores: dict) -> list[CareerArea]:
    # Sin desempate definido, no escoger una profesión por orden del JSON.
    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_dims) >= 2:
        if sorted_dims[0][1] == sorted_dims[1][1]:
            return []
        if len(sorted_dims) > 2 and sorted_dims[1][1] == sorted_dims[2][1]:
            return []
        top1, top2 = sorted_dims[0][0], sorted_dims[1][0]
        # N no se utiliza para inferir áreas profesionales.
        if "N" in (top1, top2):
            return []
        # Mantener las asociaciones directas y la búsqueda inversa existentes.
        if (top1, top2) in CAREER_MATRIX:
            return [CAREER_MATRIX[(top1, top2)]]
        elif (top2, top1) in CAREER_MATRIX:
            return [CAREER_MATRIX[(top2, top1)]]
    
    # Ausencia de regla no equivale a una recomendación de Tecnología.
    return []

def build_reporte_out(reporte: ReporteVocacional, student_name: str | None) -> ReporteOut:
    scores = reporte.scores_json
    dimensions = []
    for k, v in scores.items():
        dimensions.append(DimensionScore(
            letter=k,
            name=DIMENSION_NAMES.get(k, k),
            score=int(v * 100),
            color=DIMENSION_COLORS.get(k, "#000000"),
            interpretation=DIMENSION_INTERPRETATIONS.get(k, ""),
            vocationalImpact=VOCATIONAL_SCOPE
        ))
        
    career_areas = get_career_areas(scores)
    
    # Just format date roughly
    dt_str = "Hoy" if not reporte.created_at else reporte.created_at.strftime("%d de %b, %Y")
    
    return ReporteOut(
        studentName=student_name,
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
    return build_reporte_out(rep, estudiante.nombre_completo)

@router.get("/reporte/{reporte_id}", response_model=ReporteOut)
async def get_report_by_id(reporte_id: int, current_user: Usuario = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = (
        select(ReporteVocacional, Estudiante.nombre_completo)
        .join(ReporteVocacional.evaluacion)
        .join(Evaluacion.estudiante)
        .where(ReporteVocacional.id == reporte_id)
    )
    if current_user.rol == "estudiante":
        query = query.where(Estudiante.usuario_id == current_user.id)
    elif current_user.rol == "orientador":
        query = query.join(Estudiante.curso).join(Curso.orientador).where(
            Orientador.usuario_id == current_user.id
        )
    else:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

    result = await db.execute(query)
    row = result.one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    reporte, student_name = row
    return build_reporte_out(reporte, student_name)
