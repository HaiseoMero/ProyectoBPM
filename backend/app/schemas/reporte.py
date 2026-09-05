from pydantic import BaseModel

class DimensionScore(BaseModel):
    letter: str
    name: str
    score: int  # 0-100 percentage
    color: str
    interpretation: str
    vocationalImpact: str

class CareerArea(BaseModel):
    title: str
    desc: str
    carreras: list[str]

class ReporteOut(BaseModel):
    evaluatedAt: str
    scores: dict[str, float]
    dimensions: list[DimensionScore]
    careerAreas: list[CareerArea]
