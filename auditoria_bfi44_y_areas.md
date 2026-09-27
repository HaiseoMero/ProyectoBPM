# Auditoría Técnica del BFI-44 y Áreas Vocacionales

Este documento presenta una inspección de solo lectura sobre cómo el prototipo Vócalis implementa el inventario de personalidad BFI-44 y cómo asocia dichos puntajes con áreas vocacionales, basándose exclusivamente en el código fuente actual del repositorio.

---

## 1. Preguntas Reales del Proyecto

Las siguientes 44 preguntas son las cargadas por defecto en el sistema, obtenidas de `backend/app/seed.py` (Líneas 7-52). Todas responden a una escala Likert estándar de 5 puntos: 
(1) Muy en desacuerdo, (2) En desacuerdo, (3) Neutral, (4) De acuerdo, (5) Muy de acuerdo.

| Orden / ID | Dimensión | Inv. | Enunciado |
| :--- | :---: | :---: | :--- |
| 1 | E | No | Es sociable, conversador y expresivo. |
| 2 | A | **Sí** | Tiende a ser crítico con los demás. |
| 3 | C | No | Hace un trabajo minucioso y detallado. |
| 4 | N | No | Es deprimido, triste o melancólico con frecuencia. |
| 5 | O | No | Es original, se le ocurren ideas nuevas continuamente. |
| 6 | E | **Sí** | Es reservado, prefiere guardar las distancias. |
| 7 | A | No | Es servicial, cooperador y no busca conflictos. |
| 8 | C | **Sí** | Puede ser algo descuidado o desorganizado. |
| 9 | N | **Sí** | Es calmado, maneja bien las situaciones de estrés. |
| 10 | O | No | Tiene mucha curiosidad por temas y áreas distintas. |
| 11 | E | No | Lleno de energía, es una persona muy activa. |
| 12 | A | **Sí** | Inicia disputas o discusiones con facilidad. |
| 13 | C | No | Es un trabajador confiable y cumple sus promesas. |
| 14 | N | No | Se pone tenso o ansioso con facilidad. |
| 15 | O | No | Es ingenioso, un pensador profundo. |
| 16 | E | No | Genera mucho entusiasmo en los grupos. |
| 17 | A | No | Tiene un corazón blando, es propenso a perdonar. |
| 18 | C | **Sí** | Tiende a ser desorganizado en sus tareas escolares. |
| 19 | N | No | Se preocupa mucho por cosas sin importancia. |
| 20 | O | No | Tiene una imaginación muy activa y viva. |
| 21 | E | **Sí** | Suele ser callado o tímido ante desconocidos. |
| 22 | A | No | Tiende a confiar plenamente en las personas. |
| 23 | C | **Sí** | Tiende a ser flojo o postergar los deberes. |
| 24 | N | **Sí** | Es emocionalmente estable, difícil de alterar. |
| 25 | O | No | Es creativo, inventa soluciones diferentes. |
| 26 | E | No | Tiene una personalidad asertiva y dominante. |
| 27 | A | **Sí** | Puede ser frío o distante con sus pares. |
| 28 | C | No | Persevera hasta terminar los planes que empieza. |
| 29 | N | No | Es temperamental, cambia de humor con rapidez. |
| 30 | O | No | Valora las experiencias artísticas y estéticas. |
| 31 | E | **Sí** | A veces es tímido o le cuesta tomar la iniciativa. |
| 32 | A | No | Es considerado y amable con casi todo el mundo. |
| 33 | C | No | Hace las cosas de manera eficiente y rápida. |
| 34 | N | **Sí** | Se mantiene calmado en situaciones de alta presión. |
| 35 | O | **Sí** | Prefiere trabajos rutinarios y predecibles. |
| 36 | E | No | Es extrovertido, le agrada hacer amigos. |
| 37 | A | **Sí** | A veces es rudo o poco empático con el resto. |
| 38 | C | No | Establece planes y metas claras para su futuro. |
| 39 | N | No | Se siente nervioso o inseguro de sí mismo. |
| 40 | O | No | Le gusta reflexionar y jugar con ideas abstractas. |
| 41 | O | **Sí** | Tiene pocos intereses artísticos o científicos. |
| 42 | A | No | Le gusta cooperar en tareas comunitarias. |
| 43 | C | **Sí** | Se distrae fácilmente de sus responsabilidades. |
| 44 | O | No | Tiene sofisticación y buen gusto artístico. |

*(Nota: E=Extraversión, A=Amabilidad, C=Responsabilidad, N=Neuroticismo, O=Apertura)*

---

## 2. Implementación del Cálculo (OCEAN)

El cálculo se ejecuta centralizadamente en `backend/app/services/ocean_scorer.py`.

```python
# backend/app/services/ocean_scorer.py (Extracto Funcional)

REVERSE_ITEMS: set[int] = {2, 6, 8, 9, 12, 18, 21, 23, 24, 27, 31, 34, 35, 37, 41, 43}

def calculate_ocean_scores(answers: dict[int, int]) -> dict[str, float]:
    # ... (validaciones omitidas)
    
    # 1. Inversión de respuestas
    adjusted: dict[int, int] = {}
    for qid, val in answers.items():
        adjusted[qid] = (6 - val) if qid in REVERSE_ITEMS else val
    
    # 2. Promedio y normalización
    scores: dict[str, float] = {}
    for dim, items in DIMENSION_ITEMS.items():
        vals = [adjusted[i] for i in items]
        raw_mean = sum(vals) / len(vals)  # Rango resultante: 1.0 - 5.0
        scores[dim] = round((raw_mean - 1) / 4, 4)  # Normalizado a 0.0 - 1.0
    
    return scores
```

**Análisis de la mecánica:**
1. **Inversión (`6 - val`):** Las respuestas inversas (ej. 5 -> 1, 4 -> 2) se calculan restando el valor a 6, un estándar psicométrico.
2. **Promedio (`raw_mean`):** Se suman todos los valores ajustados de la dimensión y se dividen por su cantidad. El resultado es un valor entre 1.0 y 5.0.
3. **Conversión a Escala 0-1:** Al restar 1 y dividir por 4, la escala de 1-5 se comprime a un rango estricto de 0.0 a 1.0. 
4. **Conversión a Porcentaje (Frontend):** En `reporte.py` (línea 79), este valor flotante se convierte a un entero 0-100 mediante `int(v * 100)`.

> [!WARNING]
> **Hecho comprobado:** El cálculo devuelve un valor normalizado (0-100) basado en la puntuación máxima posible del propio instrumento. **NO es un percentil poblacional.** Un 80% en Extraversión significa "marcó opciones de extraversión el 80% de las veces", no "es más extrovertido que el 80% de la población chilena".

---

## 3. Origen y Siembra de Datos (Seed)

La base de datos se inicializa con los valores exactos definidos en la matriz del archivo `backend/app/seed.py`.

```python
# backend/app/seed.py (Extracto de Definición)

PREGUNTAS = [
    (1, 'Es sociable, conversador y expresivo.', 'E', False),
    (2, 'Tiende a ser crítico con los demás.', 'A', True),
    # ... [42 preguntas omitidas] ...
    (44, 'Tiene sofisticación y buen gusto artístico.', 'O', False),
]

# (Líneas 60-62)
# Preguntas
for orden, texto, dim, inv in PREGUNTAS:
    db.add(Pregunta(orden=orden, texto=texto, dimension=dim, es_invertida=inv))
```

**Hecho comprobado:** Si la base de datos se creó ejecutando `seed.py`, la estructura y el orden interno de IDs en MySQL refleja idénticamente la lista original, asumiendo una inserción serial con AUTO_INCREMENT partiendo en 1.

---

## 4. Asociación con Áreas de Estudio

La asignación ocurre en `backend/app/routers/reporte.py`, que cruza los resultados OCEAN con una `CAREER_MATRIX` estática.

```python
# backend/app/routers/reporte.py (Extracto)

CAREER_MATRIX = {
    ("O", "C"): CareerArea(title="Tecnología e Informática", desc="...", carreras=["Ingeniería Informática", ...]),
    ("C", "O"): CareerArea(title="Ingeniería y Gestión de Procesos", desc="...", carreras=["Ingeniería Civil Industrial", ...]),
    ("E", "A"): CareerArea(title="Comunicación y Relaciones Públicas", desc="...", carreras=["Periodismo", ...]),
    ("A", "E"): CareerArea(title="Salud y Educación", desc="...", carreras=["Medicina", ...]),
    ("O", "E"): CareerArea(title="Artes y Diseño", desc="...", carreras=["Diseño Gráfico", ...]),
    ("C", "A"): CareerArea(title="Administración y Contabilidad", desc="...", carreras=["Contabilidad", ...])
}

def get_career_areas(scores: dict) -> list[CareerArea]:
    sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_dims) >= 2:
        # Prevención de empates
        if sorted_dims[0][1] == sorted_dims[1][1]: return []
        if len(sorted_dims) > 2 and sorted_dims[1][1] == sorted_dims[2][1]: return []
        
        top1, top2 = sorted_dims[0][0], sorted_dims[1][0]
        
        # Ignora "Neuroticismo" como eje vocacional
        if "N" in (top1, top2): return []
        
        if (top1, top2) in CAREER_MATRIX: return [CAREER_MATRIX[(top1, top2)]]
        elif (top2, top1) in CAREER_MATRIX: return [CAREER_MATRIX[(top2, top1)]]
    return []
```

**Mecánica de Asociación:**
1. Se ordenan las cinco dimensiones de mayor a menor puntuación obtenida.
2. Se toman las dos más dominantes (`top1` y `top2`).
3. **Empates:** Si hay empate en el 1° lugar, o empate en el 2° lugar, la función retorna `[]` (ninguna recomendación) para evitar decisiones arbitrarias.
4. **Filtro Clínico:** Si "N" (Neuroticismo) está entre las dos más altas, se anula la asociación vocacional y retorna `[]`.
5. El sistema compara el par dominante contra `CAREER_MATRIX` en ambos órdenes. Si coincide, devuelve un único objeto `CareerArea`.
6. En el frontend, esto se renderiza como una única área. Si el array llega vacío, no se pinta ninguna sugerencia vocacional.

---

## 5. Comprobación de Coherencia y Discrepancias

Se verificó la estructura interna de `seed.py` contra `ocean_scorer.py` y el estándar BFI-44:

*   **Totalidad:** Existen exactamente 44 ítems definidos en el seed y exigidos en el scorer.
*   **Distribución de Ítems por Dimensión:**
    *   **E (Extraversión):** 8 ítems.
    *   **A (Amabilidad):** 9 ítems.
    *   **C (Responsabilidad):** 9 ítems.
    *   **N (Neuroticismo):** 8 ítems.
    *   **O (Apertura):** 10 ítems.
    *   *Suma Total:* 44. (Esta distribución es matemáticamente perfecta con el modelo oficial de John & Srivastava).
*   **Ítems Invertidos:** `ocean_scorer.py` define 16 ítems inversos. El `seed.py` define los mismos 16 ítems con `es_invertida=True`. Total coherencia entre la base de datos teórica y el motor de cálculo.
*   **Acreditación Bibliográfica (Duda):** El módulo `ocean_scorer.py` cita *"John, O. P., & Srivastava, S. (1999)"*, que es la fuente original en inglés. Sin embargo, no se cita explícitamente en el código la fuente de la traducción al español utilizada (como *Benet-Martínez & John, 1998*, versión oficial para hispanohablantes).

**Conclusión del Estado Actual:**
Desde el punto de vista puramente algorítmico, **el BFI-44 está implementado sin errores de cálculo ni de consistencia**. La sumatoria, inversión, normalización e instanciación de las preguntas son matemáticamente exactas respecto a la literatura, y los parches recientes han sellado lógicamente los fallos en empates o el uso inapropiado del Neuroticismo para sugerencias vocacionales.
