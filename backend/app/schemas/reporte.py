from pydantic import BaseModel, Field

class DimensionScore(BaseModel):
    letter: str
    name: str
    score: int  # 0-100 percentage (integer for radar/bars)
    percentage: float = 0.0  # 0.0-100.0 exact percentage
    division: int = 0  # 0..3 quartile division
    divisionLabel: str = "Bajo"  # Bajo, Medio-Bajo, Medio-Alto, Alto
    color: str
    interpretation: str
    vocationalImpact: str

class CareerArea(BaseModel):
    area_id: int | None = None
    slug: str | None = None
    title: str
    area_sies: str | None = None
    afinidad_porcentaje: float | None = None
    desc: str
    carreras: list[str]

class ReporteOut(BaseModel):
    studentName: str | None = None
    bpm_estado: str | None = None
    evaluatedAt: str
    scores: dict[str, float]
    divisiones: dict[str, int] = Field(default_factory=dict)
    codigo_base4: str = "00000"
    combinacion_id: int = 1
    total_posibilidades: int = 1024
    dimensions: list[DimensionScore]
    careerAreas: list[CareerArea]
    ranking_completo: list[CareerArea] = Field(default_factory=list)
