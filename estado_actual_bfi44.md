# Estado Actual del Inventario BFI-44 (Vócalis)

Esta revisión documenta rigurosamente la implementación del BFI-44 en el código actual del repositorio, identificando sus dependencias lógicas, mecanismos de persistencia y reglas de negocio activas, sin alterar archivos ni ejecutar migraciones.

## 1. Definición, Carga y Entrega
*   **Definición:** Los 44 enunciados, con su `orden`, `dimension` e inversión, están codificados rígidamente en una lista estática de tuplas llamada `PREGUNTAS` en **`backend/app/seed.py` (líneas 7-52)**.
*   **Carga:** En el mismo archivo **(líneas 60-62)**, el motor itera esta lista e inserta instancias del modelo SQLAlchemy `Pregunta` directamente en la base de datos al inicializar el sistema.
*   **Entrega:** Para que el estudiante los responda, el endpoint `GET /preguntas` en **`backend/app/routers/evaluacion.py` (líneas 17-22)** consulta la tabla `preguntas` ordenada por el campo `orden`, y se las entrega al frontend (Vue) con el esquema `PreguntaOut(id, text, dimension)`.

## 2. ID de MySQL vs Orden del Ítem (Acoplamiento Crítico)
*   **Estado:** El cálculo matemático está **acoplado al ID primario de MySQL**, ignorando por completo el campo semántico `orden`.
*   **Ruta de Evidencia:**
    *   En `evaluacion.py` (línea 94): Al enviar el cuestionario, se forma el diccionario `{r.preguntaId: r.valor}`. Aquí `preguntaId` es la FK que apunta al `id` autoincremental de la base de datos.
    *   En `evaluacion.py` (línea 103): Se llama a `calculate_ocean_scores(answers)`.
    *   En `ocean_scorer.py` (líneas 42-44): La función itera las llaves y lanza una excepción dura si alguna de ellas no está entre el 1 y el 44: `if not (1 <= qid <= 44): raise ValueError(...)`.
*   **Ejemplo verificable:** Si vaciamos la tabla `preguntas` con `TRUNCATE` o `DELETE` y corremos el `seed.py` de nuevo, la base de datos podría reanudar el contador y asignar los IDs del **45 al 88**. El endpoint entregaría las preguntas correctamente, pero al hacer el `POST /enviar`, el backend formaría `{45: 5, 46: 3...}` y `ocean_scorer.py` fallaría con un error **HTTP 422 ("ID de pregunta fuera de rango: 45")**, dejando la aplicación inoperable.

## 3. Coherencia Matemática y Escala
*   **Coherencia de Constantes:** Existe un 100% de coherencia. Las 16 preguntas marcadas con `es_invertida=True` en `seed.py` coinciden exactamente con la tupla `REVERSE_ITEMS` en `ocean_scorer.py` (línea 7). La suma de la variable `DIMENSION_ITEMS` (línea 9) da exactamente 44.
*   **Fórmula y Escala:** En `ocean_scorer.py` (línea 57-58), las respuestas invertidas y agrupadas se promedian (obteniendo un número entre 1.0 y 5.0) y luego se aplica la fórmula `(raw_mean - 1) / 4`.
*   **Interpretación:** Esta fórmula entrega un valor estrictamente entre 0.0 y 1.0. Luego, en `reporte.py` (línea 79), se multiplica por 100 y se castea a entero (`int(v * 100)`). Por lo tanto, **es un porcentaje del puntaje máximo teórico del test, NO es un percentil poblacional** (no te dice si eres más introvertido que el 80% de los estudiantes, solo que marcaste opciones de introversión el 80% del tiempo).

## 4. Áreas de Estudio (Reporte)
La asociación vocacional ocurre en `backend/app/routers/reporte.py` (líneas 42-70).
*   **Reglas Activas:** La función `get_career_areas(scores)` ordena las cinco dimensiones de mayor a menor. Toma el par más dominante (ej. [O, C]).
*   **Filtros de Seguridad (Decisiones del prototipo):**
    *   *Empates:* Si hay empate por el 1° lugar o empate por el 2° lugar (líneas 55-58), retorna un arreglo vacío `[]` (Sin Área).
    *   *Participación de N:* Si Neuroticismo ('N') está en el Top 1 o Top 2, retorna un arreglo vacío `[]` (línea 61).
*   **Matriz y Respaldo:** Si sobrevive a los filtros, busca el par en `CAREER_MATRIX` (línea 42). Los textos de esta matriz incluyen frases preventivas como *"Referencia exploratoria... no acredita afinidad"*. Aunque el cruce de pares Big Five coincide a grandes rasgos con los cuadrantes de Holland (RIASEC), **no existe una cita formal en el código** para la matriz exacta de 6 carreras mapeada.

## 5. Impacto de Cambios Teóricos
1.  **Cambiar solamente el texto (UPDATE sql):** No altera `ocean_scorer.py` ni las pruebas, pero las evaluaciones pasadas (`Respuesta`) siguen apuntando al mismo ID. Si un alumno abre un reporte antiguo, o el Orientador lo audita, verán el *nuevo* texto como si hubieran respondido a eso.
2.  **Cambiar el significado o dimensión:** Requeriría obligatoriamente recodificar `REVERSE_ITEMS` y `DIMENSION_ITEMS` en `ocean_scorer.py`. Los reportes emitidos antes de este cambio (guardados en `ReporteVocacional.scores_json`) quedarían intactos (inmutables), pero cualquier re-procesamiento de sus `Respuestas` originales daría un resultado diferente, causando discrepancias.
3.  **Cambiar la lógica del cálculo:** Rompería el motor y requeriría reescribir los tests automáticos (ej. `test_ocean_scorer.py`), afectando solo a las evaluaciones futuras.

## 6. Fuente de la Redacción en Español
*   **Hecho comprobado:** El archivo `ocean_scorer.py` cita en sus comentarios *"John, O. P., & Srivastava, S. (1999). The Big Five trait taxonomy."* (el original en inglés).
*   **Conclusión Verificable:** **No existe ninguna fuente, comentario, cita bibliográfica ni documentación en el repositorio** que indique de dónde proviene la redacción en español actual. No es posible asegurar mediante el código que corresponda a Benet-Martínez y John (1998) u otra validación hispana.

---

## Tabla de Resumen y Comprobaciones

| Aspecto | Estado | Rutas y Líneas de Evidencia |
| :--- | :--- | :--- |
| Enunciados y dimensión | **Confirmado en código** | `backend/app/seed.py` (Líneas 7-52) |
| Entrega a Frontend | **Confirmado en código** | `backend/app/routers/evaluacion.py` (Líneas 17-22) |
| Acoplamiento a ID BD | **Confirmado en código** | `evaluacion.py` (Líneas 94, 103) y `ocean_scorer.py` (42-44) |
| Inversión y Escala | **Confirmado en código** | `backend/app/services/ocean_scorer.py` (Líneas 7, 57-58) |
| Exclusión empates/N | **Confirmado en código** | `backend/app/routers/reporte.py` (Líneas 55-61) |
| Atribución Español | **Pendiente de comprobar** | *No existe evidencia en el repositorio.* |

### Secuencia Breve de Cambios Recomendados (Post-Análisis)
1.  **Desacoplar Cálculo:** Modificar `evaluacion.py` para que forme el diccionario de respuestas utilizando `Pregunta.orden` en lugar de `Pregunta.id` al invocar `calculate_ocean_scores()`. Esto asegura resiliencia ante recreaciones de la base de datos.
2.  **Definir Traducción:** Confirmar la traducción oficial que usará el proyecto (ej. Benet-Martínez) e incluirla en los comentarios de la matriz `CAREER_MATRIX` y `ocean_scorer.py` como referencia oficial.
3.  **Actualizar Textos (Sin romper BD):** Generar un script o migración SQL que actualice `Pregunta.texto` donde el `orden` corresponda, sin alterar la estructura y sin usar `seed.py` destructivamente.
4.  **Inmutabilidad del Historial:** Dejar registro en la documentación de que los historiales de los estudiantes anteriores al cambio de texto reflejarán los nuevos enunciados si la UI intenta volver a renderizarlos.
