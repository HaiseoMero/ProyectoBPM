"""Algoritmo de scoring del Big Five Inventory (BFI-44) y Motor Vocacional Chile (SIES).

Referencia: John, O. P., & Srivastava, S. (1999).
The Big Five trait taxonomy: History, measurement, and theoretical perspectives.
"""

from typing import Any

REVERSE_ITEMS: set[int] = {2, 6, 8, 9, 12, 18, 21, 23, 24, 27, 31, 34, 35, 37, 41, 43}
ITEMS_INVERTIDOS: set[int] = REVERSE_ITEMS

DIMENSION_ITEMS: dict[str, list[int]] = {
    "O": [5, 10, 15, 20, 25, 30, 35, 40, 41, 44],  # Openness - 10 items
    "C": [3, 8, 13, 18, 23, 28, 33, 38, 43],        # Conscientiousness - 9 items
    "E": [1, 6, 11, 16, 21, 26, 31, 36],             # Extraversion - 8 items
    "A": [2, 7, 12, 17, 22, 27, 32, 37, 42],         # Agreeableness - 9 items
    "N": [4, 9, 14, 19, 24, 29, 34, 39],             # Neuroticism - 8 items
}

MAPA_DIMENSIONES_BFI44: dict[int, str] = {
    1: "E", 2: "A", 3: "C", 4: "N", 5: "O",
    6: "E", 7: "A", 8: "C", 9: "N", 10: "O",
    11: "E", 12: "A", 13: "C", 14: "N", 15: "O",
    16: "E", 17: "A", 18: "C", 19: "N", 20: "O",
    21: "E", 22: "A", 23: "C", 24: "N", 25: "O",
    26: "E", 27: "A", 28: "C", 29: "N", 30: "O",
    31: "E", 32: "A", 33: "C", 34: "N", 35: "O",
    36: "E", 37: "A", 38: "C", 39: "N", 40: "O",
    41: "O", 42: "A", 43: "C", 44: "O",
}

DIMENSION_NAMES: dict[str, str] = {
    "O": "Apertura a la Experiencia",
    "C": "Responsabilidad (Conciencia)",
    "E": "Extraversión",
    "A": "Amabilidad",
    "N": "Neuroticismo (Estabilidad Emocional)",
}

DIVISION_LABELS: dict[int, str] = {
    0: "Bajo",
    1: "Medio-Bajo",
    2: "Medio-Alto",
    3: "Alto",
}

AREAS_CHILE: list[dict[str, Any]] = [
    {
        "id": 1,
        "slug": "informatica_datos_ti",
        "nombre": "Informática, Datos y TI",
        "area_sies": "Tecnología",
        "descripcion": "Combina alta curiosidad intelectual y apertura para resolver problemas lógicos con orden metódico y autonomía en el trabajo técnico. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 78.0, "C": 78.0, "E": 35.0, "A": 45.0, "N": 28.0},
        "pesos": {"O": 1.6, "C": 1.5, "E": 0.7, "A": 0.5, "N": 1.0},
        "carreras_ejemplo": [
            "Ingeniería Civil Informática",
            "Ciencia de Datos e IA",
            "Ciberseguridad",
            "Analista Programador",
        ],
    },
    {
        "id": 2,
        "slug": "ingenieria_civil_mineria_obras",
        "nombre": "Ingeniería Civil, Minería y Obras",
        "area_sies": "Tecnología",
        "descripcion": "Destaca por una alta exigencia en planificación, rigurosidad técnica, liderazgo de equipos en terreno y estabilidad frente a la presión operativa. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 62.0, "C": 88.0, "E": 60.0, "A": 45.0, "N": 18.0},
        "pesos": {"O": 1.0, "C": 1.8, "E": 1.0, "A": 0.6, "N": 1.5},
        "carreras_ejemplo": [
            "Ingeniería Civil en Minas",
            "Ingeniería Civil Industrial",
            "Construcción Civil",
            "Ingeniería Civil Mecánica / Eléctrica",
        ],
    },
    {
        "id": 3,
        "slug": "ciencias_basicas_exactas",
        "nombre": "Ciencias Básicas y Exactas",
        "area_sies": "Ciencias Básicas",
        "descripcion": "Se orienta a la investigación científica, el pensamiento abstracto y la experimentación rigurosa en laboratorios u observatorios. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 88.0, "C": 85.0, "E": 30.0, "A": 48.0, "N": 25.0},
        "pesos": {"O": 1.8, "C": 1.6, "E": 0.6, "A": 0.5, "N": 0.9},
        "carreras_ejemplo": [
            "Astronomía",
            "Biología",
            "Física",
            "Bioquímica",
        ],
    },
    {
        "id": 4,
        "slug": "salud_terapias",
        "nombre": "Salud y Terapias",
        "area_sies": "Salud",
        "descripcion": "Integra vocación de servicio, empatía en el trato con pacientes, apego estricto a protocolos clínicos y temple ante situaciones críticas. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 60.0, "C": 88.0, "E": 65.0, "A": 90.0, "N": 18.0},
        "pesos": {"O": 0.8, "C": 1.7, "E": 1.0, "A": 1.8, "N": 1.5},
        "carreras_ejemplo": [
            "Medicina",
            "Enfermería",
            "Kinesiología",
            "Tecnología Médica",
        ],
    },
    {
        "id": 5,
        "slug": "agropecuaria_veterinaria_medioambiente",
        "nombre": "Agropecuaria, Veterinaria y Medioambiente",
        "area_sies": "Agropecuaria",
        "descripcion": "Articula sensibilidad por los seres vivos y los ecosistemas con capacidad de gestión técnica y trabajo aplicado en terreno. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 70.0, "C": 78.0, "E": 48.0, "A": 72.0, "N": 22.0},
        "pesos": {"O": 1.2, "C": 1.3, "E": 0.7, "A": 1.3, "N": 1.1},
        "carreras_ejemplo": [
            "Medicina Veterinaria",
            "Agronomía",
            "Ingeniería Forestal",
            "Biología Marina",
        ],
    },
    {
        "id": 6,
        "slug": "administracion_negocios_finanzas",
        "nombre": "Administración, Negocios y Finanzas",
        "area_sies": "Administración y Comercio",
        "descripcion": "Combina orientación a metas, planificación estratégica y análisis financiero con habilidades de liderazgo, negociación y comunicación ejecutiva. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 60.0, "C": 85.0, "E": 80.0, "A": 45.0, "N": 20.0},
        "pesos": {"O": 0.9, "C": 1.6, "E": 1.6, "A": 0.7, "N": 1.3},
        "carreras_ejemplo": [
            "Ingeniería Comercial",
            "Auditoría",
            "Ingeniería en Control de Gestión",
            "Comercio Exterior",
        ],
    },
    {
        "id": 7,
        "slug": "derecho_gestion_publica",
        "nombre": "Derecho y Gestión Pública",
        "area_sies": "Derecho",
        "descripcion": "Requiere rigor normativo, capacidad argumentativa, pensamiento estructurado y firmeza para representar intereses o gestionar instituciones públicas. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 68.0, "C": 88.0, "E": 70.0, "A": 42.0, "N": 22.0},
        "pesos": {"O": 1.2, "C": 1.8, "E": 1.2, "A": 0.7, "N": 1.3},
        "carreras_ejemplo": [
            "Derecho",
            "Administración Pública",
            "Ciencia Política",
            "Técnico Jurídico",
        ],
    },
    {
        "id": 8,
        "slug": "educacion_pedagogias",
        "nombre": "Educación y Pedagogías",
        "area_sies": "Educación",
        "descripcion": "Destaca por una alta disposición al acompañamiento, comunicación expresiva en grupo, paciencia, empatía y planificación formativa. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 70.0, "C": 80.0, "E": 78.0, "A": 92.0, "N": 20.0},
        "pesos": {"O": 1.1, "C": 1.4, "E": 1.5, "A": 1.9, "N": 1.4},
        "carreras_ejemplo": [
            "Pedagogía",
            "Educación Parvularia",
            "Fonoaudiología",
            "Educación Diferencial",
        ],
    },
    {
        "id": 9,
        "slug": "psicologia_ciencias_sociales",
        "nombre": "Psicología y Ciencias Sociales",
        "area_sies": "Ciencias Sociales",
        "descripcion": "Une la apertura para comprender fenómenos humanos y culturales complejos con una marcada sensibilidad interpersonal y escucha activa. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 82.0, "C": 72.0, "E": 62.0, "A": 88.0, "N": 28.0},
        "pesos": {"O": 1.5, "C": 1.1, "E": 1.0, "A": 1.8, "N": 1.1},
        "carreras_ejemplo": [
            "Psicología",
            "Trabajo Social",
            "Sociología",
            "Antropología",
        ],
    },
    {
        "id": 10,
        "slug": "comunicaciones_turismo_gastronomia",
        "nombre": "Comunicaciones, Turismo y Gastronomía",
        "area_sies": "Ciencias Sociales / Administración y Comercio",
        "descripcion": "Valora el dinamismo social, la expresión creativa, la conexión con audiencias diversas y la adaptabilidad en entornos dinámicos. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 80.0, "C": 65.0, "E": 88.0, "A": 70.0, "N": 32.0},
        "pesos": {"O": 1.4, "C": 1.0, "E": 1.8, "A": 1.2, "N": 0.9},
        "carreras_ejemplo": [
            "Periodismo",
            "Relaciones Públicas",
            "Publicidad",
            "Gastronomía Internacional",
        ],
    },
    {
        "id": 11,
        "slug": "arte_diseno_arquitectura",
        "nombre": "Arte, Diseño y Arquitectura",
        "area_sies": "Arte y Arquitectura",
        "descripcion": "Se apoya fuertemente en la imaginación estética, la sensibilidad visual y espacial, y la búsqueda de lenguajes y soluciones originales. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 92.0, "C": 58.0, "E": 52.0, "A": 60.0, "N": 50.0},
        "pesos": {"O": 2.0, "C": 0.9, "E": 0.6, "A": 0.7, "N": 0.5},
        "carreras_ejemplo": [
            "Arquitectura",
            "Diseño Gráfico",
            "Artes Visuales",
            "Animación Digital",
        ],
    },
    {
        "id": 12,
        "slug": "humanidades_letras_historia",
        "nombre": "Humanidades, Letras e Historia",
        "area_sies": "Humanidades",
        "descripcion": "Prioriza la reflexión crítica, la lectura profunda, la interpretación histórica y filosófica, y el dominio del lenguaje escrito. Referencia exploratoria de las reglas del prototipo; no acredita aptitud profesional ni predice desempeño.",
        "ideal": {"O": 90.0, "C": 72.0, "E": 38.0, "A": 65.0, "N": 42.0},
        "pesos": {"O": 1.9, "C": 1.2, "E": 0.7, "A": 0.8, "N": 0.6},
        "carreras_ejemplo": [
            "Licenciatura en Historia",
            "Filosofía",
            "Literatura y Lingüística",
            "Traducción e Interpretación",
        ],
    },
]


def _validate_answers(answers: dict[int, int]) -> None:
    if len(answers) != 44:
        raise ValueError(f"Se requieren exactamente 44 respuestas, se recibieron {len(answers)}")

    for qid, val in answers.items():
        if not (1 <= qid <= 44):
            raise ValueError(f"ID de pregunta fuera de rango: {qid}")
        if not (1 <= val <= 5):
            raise ValueError(f"Valor Likert fuera de rango para pregunta {qid}: {val}")


def calcular_porcentajes_bfi44(respuestas: dict[int, int]) -> dict[str, float]:
    """Recibe un diccionario {numero_pregunta (1..44): valor_likert (1..5)}.
    Aplica inversión de ítems (6 - R) y devuelve el porcentaje (0 a 100) para O, C, E, A, N.
    """
    _validate_answers(respuestas)

    acumulado: dict[str, list[int]] = {"O": [], "C": [], "E": [], "A": [], "N": []}
    for num_pregunta, valor in respuestas.items():
        dimension = MAPA_DIMENSIONES_BFI44[num_pregunta]
        puntaje_ajustado = (6 - valor) if num_pregunta in ITEMS_INVERTIDOS else valor
        acumulado[dimension].append(puntaje_ajustado)

    porcentajes: dict[str, float] = {}
    for dim, lista_valores in acumulado.items():
        promedio = sum(lista_valores) / len(lista_valores)
        # Escalamiento Min-Max exacto de [1, 5] a [0%, 100%]: (promedio - 1) * 25
        porcentajes[dim] = round((promedio - 1.0) * 25.0, 2)

    return porcentajes


def calculate_ocean_scores(answers: dict[int, int]) -> dict[str, float]:
    """Calculate normalized OCEAN scores (0.0-1.0) from BFI-44 answers (1-5).
    Preserves compatibility with existing persistence and unit tests.
    """
    _validate_answers(answers)

    adjusted: dict[int, int] = {}
    for qid, val in answers.items():
        adjusted[qid] = (6 - val) if qid in REVERSE_ITEMS else val

    scores: dict[str, float] = {}
    for dim, items in DIMENSION_ITEMS.items():
        vals = [adjusted[i] for i in items]
        raw_mean = sum(vals) / len(vals)
        scores[dim] = round((raw_mean - 1) / 4, 4)

    return scores


def normalizar_a_porcentajes(scores: dict[str, float]) -> dict[str, float]:
    """Convierte puntajes en escala 0.0-1.0 o 0-100 a porcentajes 0.0-100.0."""
    if not scores:
        return {}
    vals = [float(v) for v in scores.values()]
    es_proporcion = all(0.0 <= v <= 1.0 for v in vals)
    factor = 100.0 if es_proporcion else 1.0
    return {k: round(max(0.0, min(100.0, float(v) * factor)), 2) for k, v in scores.items()}


def obtener_division(porcentaje: float) -> int:
    """Devuelve el índice de cuartil (0 a 3) para un porcentaje entre 0 y 100."""
    if porcentaje < 0:
        return 0
    return min(3, int(porcentaje // 25))


def obtener_etiqueta_division(division: int) -> str:
    """Devuelve la etiqueta textual de la división (Bajo, Medio-Bajo, Medio-Alto, Alto)."""
    return DIVISION_LABELS.get(division, "Bajo")


def calcular_combinacion_id(divisiones: dict[str, int]) -> int:
    """Fórmula polinómica en base 4 para obtener el ID único (1 a 1024)."""
    return (
        256 * int(divisiones["O"])
        + 64 * int(divisiones["C"])
        + 16 * int(divisiones["E"])
        + 4 * int(divisiones["A"])
        + 1 * int(divisiones["N"])
        + 1
    )


def decodificar_combinacion_id(combinacion_id: int) -> dict[str, int]:
    """Fórmula inversa: reconstruye las divisiones (0 a 3) a partir del ID (1 a 1024)."""
    if not (1 <= combinacion_id <= 1024):
        raise ValueError(f"combinacion_id debe estar entre 1 y 1024, se recibió {combinacion_id}")
    k = combinacion_id - 1
    return {
        "O": (k // 256) % 4,
        "C": (k // 64) % 4,
        "E": (k // 16) % 4,
        "A": (k // 4) % 4,
        "N": k % 4,
    }


def evaluar_perfil_vocacional(
    porcentajes_o_scores: dict[str, float],
    catalogo_areas: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evalúa un perfil OCEAN (en escala 0-1 o 0-100), calculando:
    - puntajes porcentuales (0-100)
    - divisiones discretas (0-3) y etiquetas (Bajo, Medio-Bajo, Medio-Alto, Alto)
    - código en base 4 e ID único de combinación (1 a 1024)
    - ranking de las 12 áreas de estudio de Chile (SIES) por distancia ponderada
    """
    rasgos = ["O", "C", "E", "A", "N"]
    porcentajes = normalizar_a_porcentajes(porcentajes_o_scores)
    for r in rasgos:
        porcentajes.setdefault(r, 0.0)

    div = {r: obtener_division(porcentajes[r]) for r in rasgos}
    etiquetas = {r: obtener_etiqueta_division(div[r]) for r in rasgos}
    combinacion_id = calcular_combinacion_id(div)

    areas_fuente = catalogo_areas if catalogo_areas is not None else AREAS_CHILE
    ranking_areas: list[dict[str, Any]] = []
    for area in areas_fuente:
        distancia_ponderada = sum(
            float(area["pesos"][r]) * abs(porcentajes[r] - float(area["ideal"][r]))
            for r in rasgos
        )
        suma_pesos = sum(float(v) for v in area["pesos"].values())
        afinidad = round(100.0 - (distancia_ponderada / suma_pesos), 2)
        afinidad_acotada = max(0.0, afinidad)

        ranking_areas.append({
            "area_id": area["id"],
            "slug": area["slug"],
            "nombre": area["nombre"],
            "area_sies": area["area_sies"],
            "descripcion": area.get("descripcion", ""),
            "afinidad_porcentaje": afinidad_acotada,
            "carreras_ejemplo": list(area["carreras_ejemplo"]),
        })

    ranking_areas.sort(key=lambda x: (-x["afinidad_porcentaje"], x["area_id"]))

    return {
        "puntajes": porcentajes,
        "divisiones": div,
        "etiquetas_division": etiquetas,
        "codigo_base4": f"{div['O']}{div['C']}{div['E']}{div['A']}{div['N']}",
        "combinacion_id": combinacion_id,
        "total_posibilidades": 1024,
        "top_recomendaciones": ranking_areas[:3],
        "ranking_completo": ranking_areas,
    }


def get_dominant_dimensions(scores: dict[str, float], top_n: int = 2) -> list[str]:
    """Return the top N dominant dimension letters, sorted by score descending."""
    return sorted(scores, key=lambda d: scores[d], reverse=True)[:top_n]
