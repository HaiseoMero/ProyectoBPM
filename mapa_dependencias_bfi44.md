# Mapa de Dependencias BFI-44 (Vócalis)

Este documento detalla el análisis de los componentes del repositorio que interactúan con el inventario BFI-44, desde la definición de las preguntas hasta la interfaz gráfica, incluyendo las dependencias acopladas algorítmicamente.

## 1. Definir o cargar preguntas (Texto, Orden, Dimensión, Inversión)
*   **Archivo Principal:** `backend/app/seed.py`
    *   *Detalle:* Contiene la lista de tuplas `PREGUNTAS` (Aprox. líneas 7-52) con el orden de la pregunta, el enunciado, la dimensión y un booleano indicando si es inversa. Inyecta los datos directamente en la base de datos al inicio.
*   **Modelo de Datos:** `backend/app/models/pregunta.py`
    *   *Detalle:* Define la tabla `preguntas` con las columnas `id`, `orden`, `texto`, `dimension`, `es_invertida`.

## 2. Entregar al frontend y guardar respuestas
*   **Endpoints API:** `backend/app/routers/evaluacion.py`
    *   *GET /preguntas* (Línea 17): Devuelve el array mapeando el objeto BD al esquema `PreguntaOut` (`id`, `texto`, `dimension`).
    *   *POST /respuesta* (Línea 34) y *POST /enviar* (Línea 84): Guardan objetos `Respuesta` vinculándolos al `id` de la pregunta proporcionado por el cliente en el JSON.
*   **Frontend:** `src/views/CuestionarioView.vue` y `src/services/api.js`
    *   *Detalle:* El componente solicita las preguntas, dibuja los "radios" (1-5) para cada una y gestiona el envío de payloads al backend.

## 3. Relación `pregunta.id` vs `pregunta.orden` al calcular
*   **Acoplamiento Crítico:** `backend/app/routers/evaluacion.py`
    *   *Detalle:* En la línea 94, se extrae el diccionario de respuestas: `answers = {r.preguntaId: r.valor...}`. El backend utiliza directamente la **clave primaria (id) de MySQL**.
*   **Vulnerabilidad del Cálculo:** `backend/app/services/ocean_scorer.py`
    *   *Detalle:* La función `calculate_ocean_scores` exige estrictamente que las claves del diccionario sean números del **1 al 44** (`if not (1 <= qid <= 44): raise ValueError(...)`). 
    *   **Diagnóstico:** Si la base de datos se modifica, se borran registros y se insertan de nuevo, MySQL podría generar IDs como 45-88 por el AUTO_INCREMENT. En ese escenario, **el cálculo colapsará y fallará con un error HTTP 422**, porque asume que `id` y `orden` siempre serán idénticos.

## 4. Invertir respuestas y agrupar por OCEAN
*   **Archivo:** `backend/app/services/ocean_scorer.py`
    *   *Detalle:* Define las constantes maestras `REVERSE_ITEMS` (línea 7) y `DIMENSION_ITEMS` (línea 9). Aplica la resta `(6 - val)` y calcula el promedio matemático que finalmente normaliza de 0.0 a 1.0.
    *   **Impacto de reemplazo:** Si se cambian **solo los enunciados**, este archivo *no requiere modificación alguna*. Sin embargo, si un cambio bibliográfico altera la clave de corrección (qué ítem pertenece a qué dimensión o cuál es inverso), estas constantes deben ajustarse obligatoriamente para evitar corrupción matemática en los resultados.

## 5. Guardar puntajes y construir reporte
*   **Creación del Reporte:** `backend/app/routers/evaluacion.py` (Línea 118)
    *   *Detalle:* Guarda los diccionarios pre-calculados crudos directamente en un campo JSON en MySQL mediante la instanciación de `ReporteVocacional(scores_json=scores)`.
*   **Formateo de Salida:** `backend/app/routers/reporte.py`
    *   *Detalle:* Aquí residen las definiciones puramente visuales del backend como `DIMENSION_INTERPRETATIONS`, `DIMENSION_COLORS` y se transforma el puntaje decimal (0-1) a porcentaje multiplicándolo por 100 (`int(v * 100)`).

## 6. Asociación con áreas de estudio y presentación
*   **Lógica de Reglas:** `backend/app/routers/reporte.py`
    *   *Detalle:* Define la constante `CAREER_MATRIX` y la función `get_career_areas()`. Evalúa las dimensiones más altas (excluyendo N), revisa coincidencias en ambas direcciones (ej. (O, C) o (C, O)) y maneja empates devolviendo listas vacías.
*   **Presentación:** `src/views/EvaluacionView.vue` y `src/views/StudentDashboardView.vue`
    *   *Detalle:* Reciben las áreas calculadas por el backend y renderizan las descripciones de tendencias vocacionales y el gráfico de Radar para OCEAN.

## 7. Pruebas involucradas
*   **Algoritmo y Reglas:** `backend/tests/test_ocean_scorer.py` y `backend/tests/test_career_areas.py`.
*   **Endpoints:** `backend/tests/test_evaluacion_respuestas.py` y `backend/tests/test_reportes.py`.
    *   *Impacto de reemplazo:* Reemplazar únicamente los enunciados de texto no romperá las pruebas actuales, ya que éstas operan asumiendo IDs del 1-44 y valores crudos (Likert 1-5), y no asertan contra textos descriptivos.

---

## Origen de los enunciados actuales
Se inspeccionó toda la base de código (documentación, comentarios, módulos y scripts) buscando trazas de la fuente de la traducción de las preguntas:
*   **Cita Encontrada:** `ocean_scorer.py` cita a la fuente teórica en inglés: *"John, O. P., & Srivastava, S. (1999). The Big Five trait taxonomy."*
*   **Ausencia de Traducción Oficial:** **No existe ninguna evidencia en el repositorio** (ni referencias a Benet-Martínez, ni comentarios aclaratorios) que acredite de dónde provienen las traducciones actuales al español ("Es sociable, conversador y expresivo").
*   **Conclusión:** Aunque la estructura (cantidad, distribución, reversos) es 100% fiel al BFI-44 de John & Srivastava, los textos en español no tienen un origen validado documentado en el código, lo cual representa un riesgo para la validez psicométrica y académica del sistema.

---

## Propuesta de Orden de Trabajo para Revisión de Textos

Dado que el objetivo es no corromper la información histórica (respuestas ya guardadas dependientes de IDs), ni destruir la base de datos activa:

1.  **Auditoría Externa:** Determinar la traducción oficial que se usará (ej. Benet-Martínez y John, 1998) y redactar las 44 frases exactas.
2.  **Migración de Base de Datos:** Crear un script de migración Alembic que contenga 44 sentencias `UPDATE preguntas SET texto = "..." WHERE orden = X`. Esto actualiza el registro en caliente, preservando los `id` de BD existentes, para no romper las respuestas de usuarios históricos.
3.  **Actualización del Seed:** Sustituir la lista en `backend/app/seed.py` para asegurar que las instalaciones en limpio desde cero tengan el fraseo validado.
4.  **Atribución:** Añadir un comentario en `seed.py` y una aclaración en los documentos de presentación indicando formalmente la procedencia psicométrica de la traducción.
5.  **Comprobación:** Tras aplicar el script en el entorno de desarrollo, levantar el frontend, ingresar a una cuenta de estudiante existente y confirmar visualmente que el cuestionario carga el nuevo texto, y que las respuestas previas cargadas en `/respuestas` se alinean sin error con las preguntas modificadas. No será necesario re-escribir las pruebas automatizadas del motor OCEAN.
