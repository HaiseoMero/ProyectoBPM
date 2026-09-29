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

def get_dimension_interpretation(letter: str, score_percent: int) -> str:
    descriptions = {
        "O": (
            "Tus respuestas indican una preferencia por lo familiar y lo concreto, sugiriendo comodidad en entornos estructurados.",
            "Podrías sentirte cómodo con enfoques tradicionales, aunque manteniendo cierta apertura a explorar ideas nuevas cuando es necesario.",
            "Tus resultados sugieren una inclinación hacia la curiosidad y la exploración de nuevos conceptos de forma moderada.",
            "Tus respuestas reflejan una fuerte tendencia hacia la creatividad, la imaginación y el interés por lo abstracto o novedoso.",
        ),
        "C": (
            "Tus resultados sugieren un enfoque flexible frente a las tareas, prefiriendo la espontaneidad por sobre la planificación estricta.",
            "Es posible que prefieras un equilibrio entre la flexibilidad y el orden, adaptándote a las responsabilidades sin rigidez.",
            "Tus respuestas indican una tendencia hacia la organización y el cumplimiento de metas de manera metódica.",
            "Pareces tener una fuerte orientación hacia la autodisciplina, la planificación detallada y el enfoque en objetivos a largo plazo.",
        ),
        "E": (
            "Tus respuestas sugieren una preferencia por entornos tranquilos y actividades solitarias o en grupos muy pequeños.",
            "Podrías disfrutar de interacciones sociales de forma selectiva, valorando también tus espacios de reserva y reflexión.",
            "Tus resultados indican una tendencia a disfrutar de la compañía de otros y a participar activamente en entornos sociales.",
            "Pareces sentirte muy cómodo en situaciones de alta interacción, mostrando una tendencia hacia el dinamismo y la comunicación abierta.",
        ),
        "A": (
            "Tus resultados sugieren un estilo de interacción más objetivo y competitivo, priorizando la franqueza sobre el consenso.",
            "Es posible que mantengas un equilibrio entre cooperar con otros y defender tus propios puntos de vista de manera analítica.",
            "Tus respuestas reflejan una inclinación hacia la empatía y la colaboración, buscando generalmente la armonía en tus relaciones.",
            "Pareces tener una fuerte tendencia hacia la comprensión, el apoyo a los demás y la resolución pacífica de conflictos.",
        ),
        "N": (
            "Tus respuestas indican una tendencia hacia la calma y la estabilidad emocional, sugiriendo facilidad para manejar el estrés.",
            "Podrías mantener la tranquilidad en la mayoría de las situaciones, aunque reaccionando con cierta sensibilidad ante presiones específicas.",
            "Tus resultados sugieren que podrías experimentar emociones como la preocupación o la ansiedad de manera más frecuente ante desafíos.",
            "Pareces tener una mayor reactividad emocional, lo que sugiere una tendencia a experimentar el estrés o la tensión con mayor intensidad.",
        ),
    }
    if letter not in descriptions or not 0 <= score_percent <= 100:
        return ""
    quartile = min((score_percent - 1) // 25, 3) if score_percent else 0
    return descriptions[letter][quartile]

VOCATIONAL_SCOPE = "Este puntaje por sí solo no permite inferir aptitud ni recomendar una profesión."
AREA_SCOPE = "Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño."

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

# Asociaciones exploratorias del prototipo; no equivalen a evidencia de ajuste vocacional.
CAREER_MATRIX = {
    ("O", "C"): CareerArea(
        title="Tecnología, Ciencias Básicas y Agropecuaria",
        desc="Tu perfil sugiere una combinación de curiosidad intelectual y pensamiento estructurado. Podrías sentir afinidad por campos que requieren resolver problemas complejos de forma metódica. " + AREA_SCOPE,
        carreras=["A modo exploratorio: Ingeniería Informática", "Biología", "Agronomía", "Astronomía"],
    ),
    ("O", "E"): CareerArea(
        title="Arte, Arquitectura y Humanidades (Comunicaciones)",
        desc="Tus respuestas reflejan creatividad, necesidad de expresión y energía social. Podrías encontrar interés en entornos dinámicos orientados a comunicar ideas o diseñar. " + AREA_SCOPE,
        carreras=["Solo como referencia: Arquitectura", "Diseño Gráfico", "Periodismo", "Relaciones Públicas"],
    ),
    ("O", "A"): CareerArea(
        title="Ciencias Sociales y Humanidades",
        desc="Tu perfil combina el interés por explorar nuevos conceptos con una fuerte orientación hacia la empatía y la comprensión humana. Podrías disfrutar analizando el comportamiento. " + AREA_SCOPE,
        carreras=["Por ejemplo: Psicología", "Sociología", "Antropología", "Trabajo Social"],
    ),
    ("C", "E"): CareerArea(
        title="Administración, Comercio y Derecho",
        desc="Tus resultados sugieren un enfoque organizado y orientado a metas, sumado a habilidades de persuasión e interacción. Podrías adaptarte bien a entornos de gestión o normas. " + AREA_SCOPE,
        carreras=["Para investigar: Ingeniería Comercial", "Derecho", "Administración Pública", "Auditoría"],
    ),
    ("C", "A"): CareerArea(
        title="Salud (Gestión y Cuidados) y Agropecuaria",
        desc="Tu perfil indica cuidado por el detalle, seguimiento de protocolos y una clara vocación de servicio. Es posible que te sientas cómodo en áreas de asistencia metódica. " + AREA_SCOPE,
        carreras=["A modo de referencia: Medicina", "Enfermería", "Tecnología Médica", "Medicina Veterinaria"],
    ),
    ("E", "A"): CareerArea(
        title="Educación y Salud (Atención Comunitaria)",
        desc="Tus respuestas destacan un alto dinamismo social, entusiasmo y empatía. Podrías sentir gran afinidad por profesiones centradas directamente en instruir, acompañar o sanar a otros. " + AREA_SCOPE,
        carreras=["A modo exploratorio: Pedagogía", "Educación Parvularia", "Fonoaudiología", "Kinesiología"],
    ),
}

def get_career_areas(scores: dict) -> list[CareerArea]:
    # N no participa en la asignación exploratoria; los empates conservan el orden recibido.
    sorted_dims = sorted(
        ((letter, value) for letter, value in scores.items() if letter in {"O", "C", "E", "A"}),
        key=lambda item: item[1], reverse=True,
    )
    if len(sorted_dims) >= 2:
        top1, top2 = sorted_dims[0][0], sorted_dims[1][0]
        area = CAREER_MATRIX.get((top1, top2)) or CAREER_MATRIX.get((top2, top1))
        if area:
            return [area]
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
            interpretation=get_dimension_interpretation(k, int(v * 100)),
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
