# Instrucciones para Codex: Estabilización BFI-44 (Fase 1)

Por favor, lee el contexto y ejecuta únicamente la sección de **Cambios implementables ahora**.

**Contexto:** Vócalis es un prototipo universitario (MVP ~80% funcional) que implementa el cuestionario BFI-44. Tras una auditoría estática, se ha detectado un acoplamiento crítico entre el motor matemático (`ocean_scorer.py`) y las llaves primarias (IDs) autogeneradas de MySQL.

---

## Cambios implementables ahora (Acción Requerida)

El cálculo depende incorrectamente del ID de MySQL en lugar del campo semántico `orden`. Tu objetivo es desacoplarlo para que el cálculo siga siendo correcto incluso si los IDs de las preguntas no son 1–44.

**Archivos a modificar:**
1. `backend/app/routers/evaluacion.py`

**El problema detallado:**
En el endpoint `POST /enviar` de `evaluacion.py`, se extrae el diccionario de respuestas enviado por el estudiante: `answers = {r.preguntaId: r.valor for r in request.respuestas}`. Este diccionario se envía directamente a `calculate_ocean_scores(answers)`. 
Dado que `preguntaId` es una FK del ID de MySQL, si la base de datos se regenera y la tabla de preguntas queda con IDs del 45 al 88, la función `calculate_ocean_scores` (que exige estrictamente claves del 1 al 44) colapsará lanzando un `ValueError`.

**El resultado esperado:**
1. Al recibir el request en `POST /enviar`, consulta la base de datos para obtener el mapeo entre `Pregunta.id` y `Pregunta.orden`.
2. Transforma el diccionario `answers` para que, antes de invocar a `calculate_ocean_scores()`, sus llaves sean el `orden` (1 a 44) de la pregunta, no su `id` de base de datos.
3. No alteres la lógica interna de `ocean_scorer.py`; simplemente pásale los datos en el formato que espera (diccionario de orden 1-44).

**Cómo comprobarlo:**
Crea o ajusta una prueba automatizada (`pytest`) en la suite de `evaluacion` que simule una base de datos donde las preguntas hayan sido insertadas con IDs del 50 al 93 (con órdenes del 1 al 44). Simula el `POST /enviar` de un estudiante con esos IDs altos y verifica que el cálculo se procese con éxito (HTTP 200) sin arrojar el error de "ID fuera de rango".

---

## Cambios pendientes de decisión (NO IMPLEMENTAR)

No ejecutes, modifiques ni propongas soluciones para lo siguiente todavía:
1. **Sustitución de preguntas (Traducción BFI-44):** Aún no se define la versión española académica a utilizar. No alteres `seed.py`.
2. **Actualización de Matriz de Áreas:** No toques `CAREER_MATRIX` en `reporte.py`.
3. **Migración de Respuestas Históricas:** No ejecutes un seed destructivo ni intentes crear migraciones SQL para corregir datos pasados.

---

### Recomendación para el usuario sobre GPT y Razonamiento

**Modelo Sugerido:** GPT-4o
**Nivel de razonamiento:** Ligero a Medio
**Justificación:** El error de acoplamiento de ORM (usar ID en lugar de un campo de dominio como `orden`) es un problema de arquitectura de software muy estándar y bien acotado. No requiere deducción avanzada de lógica matemática, por lo que un razonamiento ligero o medio es ideal para ir directo a la corrección del controlador en FastAPI sin intentar rediseñar el scoring completo.
