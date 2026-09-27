# Plan de Cierre MVP - Vócalis (Post-Codex)

## 1. Estado Verificado del Proyecto

He analizado el código fuente actual (`backend/app/`, `src/views/`) y evaluado los 9 puntos mencionados en la solicitud. Este es el estado real del repositorio:

*   **Arranque de Zeebe/Uvicorn (Roto):** Verificado. En `backend/app/worker.py`, `channel` y `worker` se instancian a nivel de módulo (líneas 10-11). Cuando Uvicorn hace fork de los workers sin `--reload`, el `event_loop` principal cambia, pero estas variables mantienen referencias al loop muerto, causando `Future attached to a different loop`.
*   **Error 500 por Pregunta Inexistente (Roto):** Verificado. En `backend/app/routers/evaluacion.py` (línea 59), el endpoint `/respuesta` (guardado parcial) realiza un `insert` ciego. Si el `preguntaId` es inválido (ej. 99), MySQL lanza un `IntegrityError` (500) por fallo de llave foránea. 
*   **Botón del Panel del Orientador (Roto):** Verificado. En `OrientadorDashboardView.vue`, el botón "Ver Reporte" se deshabilita condicionalmente con `:disabled="student.bpm_estado !== 'reporte_listo'"`. Si Camunda sufre una falla pero el reporte *sí* se guardó en MySQL, el orientador queda bloqueado de verlo.
*   **Ambigüedad de Cursos/Orientadores (Roto/Incompleto):** Verificado. En `auth_service.py` (línea 49-60), si hay más de 1 orientador por establecimiento, el `curso.orientador_id` queda en `NULL` (nadie ve al curso). 
*   **Controles Incompletos UI (No funcional):** Verificado. Existen botones como "Auditar" que solo lanzan un `alert()` y paginaciones estáticas en `OrientadorDashboardView.vue`.
*   **Matriz Vocacional (Implementado pero requiere giro UX):** La lógica base está en `reporte.py` retornando arreglos neutros, pero la UI en Vue sigue hablando de "Áreas profesionales" como si fuesen determinantes.

### Correcciones a los resúmenes anteriores (.md)
*   *Implementation_plan2.md* sugiere una estructura de concurrencia y persistencia de Zeebe que ya fue resuelta e implementada exitosamente por Codex a través del patrón Outbox (`bpm_service.py` y MySQL transaccional).
*   *Resumen_proyecto.md* puede insinuar que el MVP está listo, pero el problema del "event loop" impide que el sistema arranque consistentemente en un servidor de producción normal (sin `--reload`).

---

## 2. Decisiones que Requieren Criterio

**Decisión 1: Asignación de Estudiantes con Múltiples Orientadores**
*   *Alternativa A:* Crear una interfaz para que cada orientador "reclame" o se asigne cursos manualmente tras registrarse. (Requiere crear nuevos endpoints, tablas intermedias y vistas en Vue).
*   *Alternativa B:* **(Recomendada para el MVP)** Modificar el alcance de acceso a nivel de *Establecimiento*. Eliminar la llave foránea `orientador_id` de `Curso`. En `orientador.py`, un orientador podrá ver a todos los estudiantes de los cursos que pertenezcan a su mismo establecimiento. Esto resuelve la ambigüedad inmediatamente, fomenta la colaboración entre orientadores del mismo colegio y no retrasa el MVP.

**Decisión 2: Fundamentación y Presentación Vocacional**
*   *Alternativa A:* Mantener el término "Recomendaciones Profesionales" e inventar un cruce estricto. (Peligroso éticamente y sin sustento científico sólido para un MVP simple).
*   *Alternativa B:* **(Recomendada para el MVP)** Cambiar el enfoque descriptivo en el frontend. En lugar de "Áreas profesionales sugeridas", llamarlo **"Tendencias de Interés (Modelo RIASEC)"**. Añadir un texto fijo en la UI: *"Estas tendencias son un reflejo de tus afinidades conductuales y sirven para guiar tu exploración, no constituyen un diagnóstico de aptitud para una carrera específica."*

---

## 3. Plan por Etapas (Orden de Dependencia)

### Etapa 1: Estabilización Backend Crítica (Bloqueante)
1.  **Fix Zeebe Worker Loop:** Mover la instanciación de `channel = create_insecure_channel(...)` y `worker = ZeebeWorker(channel)` dentro de la función asíncrona `start_worker()` en `worker.py`. 
    *   *Resultado:* Uvicorn arranca impecablemente sin `--reload`.
2.  **Manejo de Errores FK en Respuestas Parciales:** En `/respuesta` (`evaluacion.py`), capturar explícitamente `IntegrityError` o validar que `preguntaId` esté entre 1 y 44 antes de hacer el `upsert`. Retornar un error `400 Bad Request`.
    *   *Resultado:* El servidor no lanza 500 al recibir payloads alterados.
3.  **Refactor Visibilidad Orientador (Decisión 1):** Actualizar `auth_service.py`, el modelo `Curso` y `orientador.py` para que la consulta cruce por `Establecimiento` y no por asignación estricta de 1 a 1.
    *   *Resultado:* Múltiples orientadores del mismo colegio ven a todos sus alumnos.

### Etapa 2: Pulido de UX y Lógica de Interfaz Frontend
4.  **Desacoplar Botón de Reporte del Estado BPM:** En `OrientadorDashboardView.vue`, cambiar la lógica `:disabled`. El backend ya expone si existe reporte. Habilitar el botón si el reporte existe en la base de datos, independiente de si el evento BPM se atoró.
5.  **Limpieza de UI Incompleta:** Eliminar el botón "Auditar", funciones que lanzan `alert()` y la paginación ficticia en el panel del orientador. Simplificar para el MVP.
6.  **Ajuste Semántico del Reporte (Decisión 2):** En `EvaluacionView.vue` y `StudentDashboardView.vue`, cambiar títulos de "Recomendaciones" a "Áreas de Exploración Sugeridas" e incluir el *disclaimer* ético/académico.

### Etapa 3: Preparación para Entorno Real
7.  **Script de Reconstrucción (Clean Install):** Crear un `Makefile` o script `setup.sh` que destruya contenedores viejos, levante Docker Compose, aplique migraciones Alembic de cero e inserte el `seed` no destructivo (solo `Preguntas` base).
8.  **Verificación de Diseño (Responsive):** Ajustes CSS finales para asegurar que el radar y las tablas se vean bien en móviles (pantallas < 768px).

---

## 4. Estrategia de Verificación

*   **Prueba de Arranque (Backend):** Ejecutar `uvicorn app.main:app --host 0.0.0.0` (sin `--reload`) y asegurar que no hay stacktraces asíncronos.
*   **Pruebas Manuales (Navegador):**
    *   Ingresar con 2 orientadores distintos usando el mismo código de colegio. Asegurar que ambos ven a los alumnos creados por el colegio.
    *   Apagar el contenedor de Zeebe a propósito. Terminar el cuestionario como alumno. Comprobar que el reporte se guarda en MySQL, el orientador lo puede ver (botón habilitado) a pesar de que el proceso BPM diga "incierto/pendiente".
*   **Métricas Pendientes (A realizar por ti):** 
    *   *Rendimiento:* Usar una herramienta sencilla como `locust` (opcional) o realizar peticiones concurrentes para comprobar los 30 usuarios simultáneos.
    *   *Usabilidad:* Sesión de 15 minutos con 5 usuarios reales (fuera del alcance del código, pero necesario para tu tesis).
