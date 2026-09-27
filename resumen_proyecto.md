# Resumen del Proyecto — Vócalis (ProyectoBPM)

> **Propósito de este documento:** Servir como contexto completo para una herramienta de IA (Codex u otra) que retome el desarrollo del proyecto. Estado contrastado con el código al **27 de septiembre de 2026**. Las cifras de pruebas y cobertura proceden de la ejecución completa del 27/09/2026 con MySQL aislado. Se distinguen funcionalidades implementadas, límites verificados y pendientes. El plan final es una referencia histórica, no una descripción del estado actual.

---

## 1. Qué es el Proyecto

**Vócalis** es una aplicación web de orientación vocacional para estudiantes de enseñanza media en Chile. Su flujo principal es:

1. El estudiante se registra y queda asociado a un curso. El orientador se obtiene mediante ese curso cuando tiene uno asignado; los cursos sin asignación se asocian automáticamente solo cuando hay exactamente un orientador del establecimiento.
2. Completa el cuestionario psicométrico **BFI-44** (Big Five Inventory, 44 ítems con escala Likert de 5 puntos).
3. La API calcula los puntajes en las 5 dimensiones de personalidad **OCEAN** (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).
4. Se genera un **reporte vocacional** con gráfico de radar, descripciones OCEAN en español y referencias profesionales exploratorias cuando las reglas existentes lo permiten; en otro caso presenta un resultado neutral.
5. El **orientador escolar** accede a un panel de monitoreo para ver el progreso y reportes de sus estudiantes asignados.

**Camunda 8 (Zeebe)** representa el seguimiento BPM del cuestionario mediante un `receiveTask` y tres workers. El cálculo OCEAN y la creación del reporte ocurren en la API, no en Camunda. La entrega posterior al commit y la recuperación mediante outbox están implementadas. El recorrido HTTP con MySQL y Zeebe reales pasó sin `--reload`, incluida una caída y recuperación del broker. Firefox 156.0.1 recorrió ambos roles en escritorio y móvil; las sesiones de usabilidad con personas siguen pendientes.

**Contexto académico:** Este es un Proyecto de Título de Ingeniería en Informática (2026). El documento oficial del proyecto es `docs/WordBPM.docx`.

---

## 2. Stack Técnico Completo

### Backend

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **Python** | 3.11+ (runtime actual: 3.14) | Lenguaje del backend |
| **FastAPI** | ≥0.115 | Framework web (ASGI) |
| **Uvicorn** | ≥0.30 (standard) | Servidor ASGI |
| **SQLAlchemy** | ≥2.0 (asyncio) | ORM asíncrono |
| **Pydantic** | ≥2.0 | Validación de schemas |
| **pydantic-settings** | ≥2.6 | Gestión de configuración vía `.env` |
| **python-jose** | ≥3.3 (cryptography) | Creación/verificación de tokens JWT |
| **bcrypt / passlib** | ==4.0.1 / ≥1.7 | `security.py` usa bcrypt directamente; passlib sigue declarado como dependencia |
| **PyZeebe** | ≥4.0 | Cliente gRPC para Camunda 8 / Zeebe |
| **aiomysql** | ≥0.2 | Driver async para MySQL |
| **aiosqlite** | ≥0.22.1 | Driver async para SQLite en tests; declarado en `backend/requirements.txt` |
| **Alembic** | ≥1.14 | Cadena `20260922_eval_unique` → `20260922_registro_contexto` → `20260924_bpm_outbox`; aplicación en desarrollo registrada y migraciones probadas en MySQL aislado |
| **Pytest** | ≥8.0 | Framework de testing |
| **pytest-asyncio** | ≥0.24 | Soporte async para pytest |
| **httpx** | ≥0.27 | Cliente HTTP async (para tests) |
| **email-validator** | ≥2.0 | Validación de formato de emails |

### Frontend

| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **Vue.js** | ^3.5.32 | Framework SPA (Composition API, `<script setup>`) |
| **Vue Router** | ^5.0.4 | Enrutamiento con navigation guards |
| **Axios** | ^1.18.0 | Cliente HTTP (instancia centralizada en `src/services/http.js`) |
| **Vite** | ^8.0.8 | Bundler y dev server |
| **ESLint** | ^10.2.1 | Linting JavaScript/Vue |
| **Prettier** | 3.8.3 | Formateo de código |
| **OxLint** | ~1.60.0 | Linter rápido complementario |

### Infraestructura (Docker Compose)

| Servicio | Imagen | Puerto |
|---------|--------|--------|
| **MySQL** | `mysql:8.0` | 3306 |
| **Elasticsearch** | `elasticsearch:8.15.3` | 9200 |
| **Zeebe** (Camunda 8) | `camunda/zeebe:8.6.7` | 26500 (gRPC), 9600 |
| **Operate** | `camunda/operate:8.6.7` | 8081 |
| **Tasklist** | `camunda/tasklist:8.6.7` | 8082 |
| **Backend** | Build local (`./backend`) | 8000 |

### Entorno de desarrollo

- **OS:** CachyOS (Arch Linux)
- **Node:** ^20.19.0 || ≥22.12.0
- **Control de versiones:** Git + GitHub
- **IDE:** Visual Studio Code

---

## 3. Decisiones de Arquitectura y Razones

### Tabla `usuario` unificada con campo `rol` → Sin herencia de tablas

**Decisión:** Una sola tabla `usuario` con `RolEnum(estudiante, orientador)` + tablas de perfil (`estudiante`, `orientador`) enlazadas 1:1 vía `usuario_id`.

**Razón:** Evita la complejidad de herencia de tablas (Joined Table Inheritance) en SQLAlchemy async. Un único modelo maneja la autenticación para ambos roles. Las tablas de perfil solo almacenan datos específicos del rol (`nombre_completo`, `edad`, `departamento`, etc.).

---

### Asignación estudiante-orientador automática vía tabla `curso`

**Decisión:** El estudiante indica establecimiento, nivel y letra. El curso se busca por `establecimiento + nombre`, combinación protegida por `uq_curso_establecimiento_nombre`. La relación sigue siendo `Orientador 1:N Curso N:1 Estudiante`, sin rol Administrador.

**Asignación:** al registrar un estudiante se asigna su curso, si está libre, únicamente cuando existe exactamente un orientador del establecimiento. Al registrar un orientador, si es el único, se asignan los cursos libres de ese establecimiento. Con cero o varios orientadores no se elige uno arbitrariamente; las asociaciones existentes siempre se conservan. Compartir establecimiento no concede permisos: los endpoints siguen comprobando `curso.orientador_id`. El registro es atómico, usa `SERIALIZABLE` en MySQL, bloqueos y hasta ocho intentos acotados ante conflictos; el hash y la verificación bcrypt se ejecutan fuera del event loop. La resolución de cursos ambiguos sigue pendiente.

### Registro por rol y datos históricos

- **Orientador:** requiere establecimiento y código privado `ORIENTADOR_REGISTRATION_CODE`. Sin configuración, vacío o solo espacios, devuelve 403; no hay secreto público predeterminado. Se usa `SecretStr` y `hmac.compare_digest` antes de crear el usuario. El código no se almacena ni se devuelve; los errores de validación omiten los inputs. El formulario lo solicita solo para orientadores y lo limpia tras el envío.
- **Estudiante:** requiere fecha de nacimiento ISO sin hora, establecimiento, nivel y letra. Se rechazan fechas inválidas, de hoy/futuras y edades superiores a 120 años. La edad se calcula considerando el cumpleaños. `Estudiante.edad` deriva de la fecha cuando existe; de lo contrario usa `_edad_historica`, mapeada a la columna existente `edad`. No se inventan fechas para alumnos antiguos ni se expone la fecha en `/auth/me`.
- El frontend envía campos exclusivos del rol elegido. Tras registrarse vuelve al formulario de login, sin afirmar inicio automático; JWT y redirecciones por rol se conservan.

---

### Test BFI-44 de una sola oportunidad

**Decisión:** Cada estudiante solo puede completar el cuestionario una vez. La validación del router (lógica en `evaluacion.py`) se refuerza con la restricción UNIQUE `uq_evaluacion_estudiante` sobre `evaluacion.estudiante_id`.

**Razón de diseño:** Mantener un único intento dentro del MVP simplifica la UI y la relación entre evaluación y reporte. La aplicación reutiliza la evaluación existente y rechaza edición/reenvío cuando su estado es `completada` o `procesada`; la BD garantiza una sola fila por estudiante. El guardado bloquea estudiante/evaluación y el envío bloquea la evaluación con `FOR UPDATE`. Dos envíos y despachadores concurrentes se probaron en MySQL; no se extrapola desde SQLite ni a todas las intercalaciones posibles.

> **Resuelto:** El modelo declara `UniqueConstraint("estudiante_id", name="uq_evaluacion_estudiante")`. La migración Alembic `20260922_eval_unique` se aplicó después de comprobar que las 2 evaluaciones existentes no tenían duplicados; ambas se conservaron y se verificó el índice UNIQUE en MySQL.

---

### Exclusiones del MVP

| Excluido | Razón |
|----------|-------|
| **Exportación PDF** | Complejidad de renderizado server-side fuera del alcance del proyecto académico |
| **Analítica predictiva** | Requiere datos históricos masivos que no existen en un MVP |
| **Rol Administrador** | La asignación automática vía `curso` elimina la necesidad de gestión administrativa manual |
| **Tests automatizados de frontend** | Fuera del requisito original; existen cuatro pruebas acotadas de presentación del reporte, sin constituir E2E de navegador |

---

### receiveTask en vez de userTask en BPMN

**Decisión:** El BPMN usa `receiveTask` (mensaje `CuestionarioCompletado`) en vez de `userTask` para la tarea del cuestionario.

**Razón:** El cuestionario se resuelve en Vue y la API publica `CuestionarioCompletado`, sin depender de una interfaz Tasklist para responder. El envío validado es la fuente de verdad: calcula OCEAN y confirma respuestas definitivas, reporte, `completed_at` y evento `completar` en una transacción MySQL; **sólo después** publica el mensaje. Si falla el commit, no publica; si falla Zeebe, conserva el reporte y el evento recuperable. `start_process()` prepara proceso/evento `iniciar` sin commit interno ni RPC. Los workers validan reporte/instancia y avanzan estados sin retroceder. No hay transacción distribuida ni garantía ilimitada de exactly-once.

---

## 4. Qué se ha Implementado

### Backend — FastAPI

| Componente | Estado | Detalle |
|-----------|--------|---------|
| **Autenticación JWT** | Implementado | Login, registro y `/auth/me`. JWT HS256 con `sub`, `role`, `exp` y expiración configurable (24 h por defecto), sin cambio de formato. Login y requests rechazan `is_active=False`, incluidos tokens previamente emitidos. Registro protegido y asignación por establecimiento implementados; pruebas permanentes de registro, login/is_active y autorización por curso (§Testing). |
| **RBAC y reportes** | Implementado y probado | Consulta propia para estudiante; por ID sólo propietario u orientador de sus cursos (404 ajeno/inexistente). Ruta específica del orientador: 403 si el alumno no pertenece y 404 si no tiene reporte. Tests de JWT inválidos, inactivos, pertenencia y contrato común; casos propios/ajenos también probados por HTTP real. |
| **Cuestionario BFI-44** | Implementado y probado | Recuperación sólo de respuestas propias, sin crear evaluación. Envío exige 44 entradas, enteros estrictos, Likert 1–5, sin duplicados y conjunto exacto de preguntas; errores controlados 422. El payload final reemplaza el borrador y genera el reporte en una transacción. Guardado/envío bloquean filas; completadas/procesadas se rechazan. El guardado individual consulta los IDs reales, devuelve 422 si faltan y reintenta deadlocks MySQL acotadamente antes de un 503 controlado. |
| **Cálculo OCEAN** | Implementado | `ocean_scorer.py`: 16 ítems invertidos, normalización 0–1 y cinco dimensiones. Se ejecuta en `routers/evaluacion.py`. `get_dominant_dimensions()` existe, pero no tiene un consumidor efectivo en el flujo actual. |
| **Generación/consulta de reportes** | Implementado y probado; contenido histórico no versionado | `scores_json` persistido; `ReporteOut` compartido con identidad real. Descripciones españolas y límites de inferencia. Seis pares existentes de `CAREER_MATRIX`, búsqueda directa/inversa, sin fallback a Tecnología. Devuelve `[]` ante regla ausente, datos insuficientes, N entre las dos mayores o empate que impide ordenar las dos primeras. No se añadieron asociaciones ni se acreditó validez académica. |
| **Estado de evaluación** | Implementado | `GET /api/evaluacion/estado`: estado de evaluación, `bpm_estado`, fechas y orientador. `completed_at = func.now()` se asigna antes del commit al completar; no se rellenaron fechas históricas. Edición y reenvío de `completada`/`procesada` se rechazan. |
| **Panel del orientador** | Implementado y probado en API y Firefox | Filtrado por cursos y reporte autorizado. Expone `bpm_estado` original; retirados `bpmStatus/statusClass` sin consumidores. `lastUpdate` se conserva para el frontend: contiene inicio de evaluación y la columna dice «Inicio de evaluación». Ocho tests prueban estados, contrato y reporte disponible antes de `reporte_listo`. |
| **Integración Zeebe** | Implementada y probada sin recarga | `ZEEBE_GATEWAY`, `process_instance_key` persistida, outbox durable, reintentos y logging JSON; workers idempotentes. E2E real aprobado sin `--reload`; worker y cliente gRPC se crean en el loop activo, se cierran al apagar y los fallos de tareas quedan observables (§Testing). Workers no calculan OCEAN ni notifican externamente. |
| **Seed de datos** | Implementado, destructivo | 44 preguntas coherentes con dimensiones/inversiones del scorer, un orientador, tres cursos y un estudiante demo. El orientador comparte establecimiento con sus cursos; el alumno demo conserva edad histórica y fecha NULL. Compatible con el nuevo esquema, probado solo en MySQL temporal. Borra y recrea tablas del modelo; no es una migración incremental. |

### Frontend — Vue.js 3

| Vista | Estado | Detalle |
|-------|--------|---------|
| **`homeview.vue`** | Geometría corregida en código | Radar decorativo de cinco ejes con cuadrícula pentagonal; nombre `HomeView` fijado para lint. Datos ilustrativos; textos de personalización/compatibilidad más amplios que el contrato actual. |
| **`AuthView.vue`** | Implementado con límites | Login/registro por rol, establecimiento enviado, fecha de nacimiento para estudiantes y código privado para orientadores. Limpieza del código y errores comprensibles; al registrarse se solicita iniciar sesión. |
| **`StudentDashboardView.vue`** | Probado en Firefox escritorio/móvil | Datos reales de reporte, identidad de `/auth/me`, iniciales y fechas de estado, sin porcentajes/área fijos. `#history-section` activa la bitácora. Error de `getEstado()` visible aunque cargue el reporte. BPM desde mapeo común; sin sondeo continuo. |
| **`EvaluacionView.vue`** | Correcciones recientes implementadas | Preguntas reales, bloques de diez, recuperación de respuestas y primer bloque incompleto. Guardado individual en orden, selección local conservada ante fallos, reintento y aviso al abandonar con cambios pendientes. Envío final espera los guardados. Evaluaciones terminadas no muestran edición y ofrecen acceso al reporte. BPM mediante estado real y mapeo compartido. |
| **`ReporteView.vue`** | Probado en Firefox escritorio/móvil | Servicio según rol/ruta, identidad e iniciales reales, sin recomendación ni finalización BPM ficticias. Radar O,C,E,A,N de cinco ejes separados 72°, puntajes buscados por letra y cuadrícula pentagonal; independiente del orden JSON. `careerAreas: []` muestra resultados neutrales. PDF fuera del MVP y sin botón decorativo. Etiquetas del radar móvil sin superposición. Cuatro tests de plantilla y recorrido real de navegador. |
| **`OrientadorDashboardView.vue`** | Probado en Firefox escritorio/móvil | Datos, filtros/contadores reales y ruta de reporte para orientador. Carga, error, reintento y vacíos diferenciados. «Inicio de evaluación» describe `created_at`. «Ver Reporte» usa `hasReport` derivado en la lista autorizada por curso, incluso con BPM pendiente; se retiraron «Auditar» y la paginación decorativa. Carga, error y reintento probados en Firefox. Sin sondeo continuo. |

### Flujo de reportes y reanudación

- **Estudiante:** `/estudiante/reporte` → `reporteService.getLatestReport()` → `GET /api/evaluacion/reporte`.
- **Orientador:** `/orientador/estudiante/:studentId/reporte` (nombre `orientador-reporte`, guard de rol orientador) → `orientadorService.getStudentReport()` → `GET /api/orientador/estudiante/{estudiante_id}/reporte`. No utiliza una ruta exclusiva de estudiantes ni elude la autorización del backend.
- **Reporte compartido:** los endpoints anteriores y la consulta por ID usan `ReporteOut` y `build_reporte_out()`, incluido el nombre del estudiante evaluado.
- **Reanudar:** `EvaluacionView` carga preguntas, respuestas persistidas y estado antes de permitir editar. Recupera selecciones y abre el primer bloque incompleto; si todos están respondidos, abre el último. No crea una evaluación al leer.
- **Guardar/salir:** la cola mantiene las peticiones individuales en orden dentro de esa vista. Ante fallo, conserva los valores locales, marca lo pendiente y permite reintentar. La navegación espera los guardados y advierte si quedan cambios; también hay aviso `beforeunload`. Los cambios no confirmados no se convierten en un borrador persistente: si se acepta abandonarlos, pueden perderse.
- **Finalizar:** espera la cola, exige que no queden respuestas sin guardar y navega al reporte tras el envío exitoso. El servidor valida y persiste 44 respuestas definitivas con reporte y outbox bajo bloqueo. La prueba MySQL de dos envíos simultáneos obtiene 200/400 y un único reporte/evento.

### Base de Datos

| Tabla | Estado | Columnas clave |
|-------|--------|---------------|
| `usuario` | ✅ | `id`, `email` (unique), `hashed_password`, `rol` (enum), `is_active`, `created_at` |
| `estudiante` | ✅ | `id`, `usuario_id` (unique FK), `nombre_completo`, `edad` histórica, `fecha_nacimiento` nullable, `curso_id` (FK) |
| `orientador` | ✅ | `id`, `usuario_id` (unique FK), `nombre_completo`, `departamento`, `establecimiento` nullable |
| `curso` | ✅ | `id`, `nombre`, `establecimiento`, `orientador_id` (FK); UNIQUE (`establecimiento`, `nombre`) |
| `evaluacion` | ✅ | `id`, `estudiante_id` (FK, UNIQUE `uq_evaluacion_estudiante`), `estado` (enum), `created_at`, `completed_at` |
| `pregunta` | ✅ | `id`, `texto`, `dimension` (enum OCEAN), `es_invertida`, `orden` (unique) |
| `respuesta` | ✅ | `id`, `evaluacion_id` (FK), `pregunta_id` (FK), `valor` (check 1-5), unique(evaluacion_id, pregunta_id) |
| `reporte_vocacional` | ✅ | `id`, `evaluacion_id` (unique FK), `scores_json`, `carreras_json`, `interpretaciones_json` |
| `proceso_bpm` | ✅ | `id`, `evaluacion_id` (unique FK), `process_instance_key`, `estado_actual`, `updated_at` |
| `bpm_evento` | ✅ | Outbox: `evaluacion_id`, `tipo`, UUID `message_id`, `estado`, `intentos`, fechas de intento y error; UNIQUE evaluación/tipo y message_id |

### BPM / Camunda 8

| Componente | Estado verificado |
|-----------|-------------------|
| `bpmn/evaluacion-vocacional.bpmn` | BPMN original desplegado y ejecutado en Zeebe 8.6.7 aislado: dos publicaciones y seis jobs completados en la demo final. No acredita despliegue vigente en otro entorno. |
| Docker Compose | Configura MySQL, Zeebe, Operate, Tasklist, Elasticsearch y backend; usa `zeebe:26500`. |
| Workers Zeebe | Integrados al lifespan; validan reporte/clave de instancia y avanzan idempotentemente. Arranque/avance probados con Uvicorn normal, sin recarga; canal y worker se crean en el loop activo y se cierran al apagar. |
| Mensaje `CuestionarioCompletado` | Reporte/evento confirmados antes de publicar. Outbox y reintentos conservan reporte ante caída; logging JSON. Fallos de commit/publicación probados por suite; caída/reinicio reales probados sin `--reload`. |
| Clave y configuración | `process_instance_key` correctamente mapeado; cliente/worker usan `settings.ZEEBE_GATEWAY` (`localhost:26500` local). `ZEEBE_ADDRESS` no es configuración efectiva. |

La entrega técnica de `bpm_evento` (`pendiente`, `incierto`, `enviado`, `consumido`, `revision`) es distinta de `bpm_estado`. Reintento cada 5 s con espera hasta 300 s, RPC limitado a 5 s, UUID estable, TTL 24 h y ventana automática 23 h. `FOR UPDATE SKIP LOCKED` coordina despachadores. Inicios ambiguos e históricos necesitan conciliación; véase `backend/BPM_RECOVERY.md`.

`src/utils/bpmStatus.js` comparte el siguiente mapeo entre StudentDashboardView, OrientadorDashboardView y EvaluacionView:

| Estado persistido | Etiqueta frontend | Productor |
|-------------------|-------------------|-----------|
| `registro` | Registro | Valor inicial del modelo y `start_process()` |
| `calculando_ocean` | Calculando perfil | Worker `calcular-ocean` |
| `generando_reporte` | Generando reporte | Worker `generar-reporte` |
| `reporte_listo` | Reporte disponible | Worker `notificar-orientador` |

Null, ausente o desconocido → **Estado no disponible**, sin progreso activo inferido. `ReporteView` mantiene un mensaje neutro porque su contrato no entrega estado BPM. Los valores retornados por workers (`ocean_calculado`, `reporte_generado`, `notificado`) no son estados persistidos del proceso. `procesada` pertenece al enum de evaluación, pero ningún productor actual lo asigna.

### Testing

| Archivo/componente real | Estado y cobertura |
|-------------------------|--------------------|
| `backend/tests/conftest.py` | SQLite para tests rápidos; los bloqueos/concurrencia se prueban aparte con MySQL. |
| `test_ocean_scorer.py` | 4 tests; no exhaustivos para todas las inversiones y dimensiones. |
| `test_evaluacion_unique_migration.py` | 3 tests de preservación y unicidad. |
| `test_evaluacion_respuestas.py` | 35 casos: autorización, recuperación, bloqueo, payloads inválidos y coherencia del envío definitivo. |
| `test_auth_registro.py` | 37 casos: registro por rol/código, fecha/edad, login e inactivos, cursos/asignación, permisos y rollback. |
| `test_registro_migration.py` | 2 tests de datos antiguos, unicidad y duplicados. |
| `test_registro_mysql.py` | 5 opcionales MySQL: concurrencia, asociación, migración histórica y seed en BD aislada. |
| `test_bpm_delivery.py` | 15 pruebas de commit/publicación, reintentos, UUID estable, solicitudes repetidas, inicio incierto y avance. Gateway inaccesible real; broker simulado para aceptación. |
| `test_bpm_mysql.py` | 4 opcionales MySQL: dos envíos, despachadores competidores y migración outbox; Zeebe simulado aquí. |
| `test_reportes.py` | 53 casos de permisos, JWT inválidos/inactivos, reportes inexistentes, contrato de tres endpoints y neutralidad histórica. |
| `test_career_areas.py` | 29 casos de pares existentes/inversos/no cubiertos, N, insuficiencia y empates. |
| `test_orientador_estado.py` | 8 casos de estados, fecha y contrato sin mapeos antiguos. |
| `test_worker_lifecycle.py` | 3 casos de loop activo, cierre del canal/cliente y observabilidad de fallos. |
| `tests/frontend/reporte-neutral.test.mjs` | 4 tests de plantilla con/sin áreas para ambos roles; no comprueban navegador ni navegación. |
| `backend/scripts/validate_mvp.py` | Validador HTTP/MySQL/Zeebe aislado: migración, BPMN, registro, BFI-44, reportes y caída/recuperación. |

**Última ejecución verificada (27/09/2026): 198 backend aprobadas, 0 omitidas y 0 fallidas**, incluidas **nueve MySQL** (cinco de registro y cuatro BPM). Sin `VOCALIS_TEST_MYSQL_ADMIN_URL` pueden omitirse nueve; no contarlas como aprobadas. Las cifras **76 aprobadas/4 omitidas** de Antigravity, **80** de Codex y **98** de la etapa de recuperación son antecedentes históricos.

**Cobertura medida**, no derivada del número de tests: **917/1004 líneas = 91,33 %; 175/212 ramas = 82,55 %; combinación coverage.py = 89,80 %**. Medición con coverage.py 7.16.1 sobre todo `backend/app`, sin excluir archivos de baja cobertura; tests y migraciones quedan fuera del denominador. `main.py` alcanza 96 % y `worker.py` 44 % en pytest; el recorrido real de Zeebe se acreditó aparte. La demo externa no se sumó a ese porcentaje. Evidencia actual: `/tmp/vocalis-stage2-coverage.json`.

**E2E API/BD/broker:** 26 comprobaciones aprobadas sin `--reload` con MySQL 8.0.46 y Zeebe 8.6.7 aislados, incluido reporte accesible para el orientador con BPM aún en `registro`, caída/reintento del broker y evento `consumido`. La instalación aislada aplicó Alembic tras `Base.metadata.create_all` y cargó sólo las 44 preguntas; la cadena aún carece de migración inicial completa. Evidencia: `/tmp/vocalis-demo-58l1stz4/checks.json` y `docs/validacion_mvp.md`.

**Frontend y carga:** cuatro pruebas de plantilla, build y ESLint dirigido a cuatro vistas aprobados. Firefox 156.0.1 (Linux, headless) completó 34 verificaciones de ambos roles a 1440×900 y 390×844 sobre el build, más carga/error/reintento del panel; capturas en `/tmp/vocalis-browser-stage2-20260927/`. Una corrida HTTP de 30 usuarios terminó 30/30 recorridos, 1500 solicitudes, 0 errores, p95 por operación ≤1,216 s y máximo ≤1,276 s; no mide renderizado ni finalización BPM. Las sesiones de usabilidad con cinco personas no se han realizado.

---

## 5. Bugs Corregidos Relevantes

| Bug | Dónde | Solución |
|-----|-------|----------|
| **Autenticación con bcrypt** | `security.py`, `requirements.txt` | bcrypt está fijado a 4.0.1; el código actual usa sus funciones directamente. |
| **Logout no redirigía** | `authService.js` | Se cambió `router.push` por `window.location.replace('/auth')` para limpiar estado Vue |
| **Email-validator faltante** | `requirements.txt` | Se agregó `email-validator>=2.0` (requerido por Pydantic `EmailStr`) |
| **Reinicialización de datos demo** | `seed.py` | Usa `drop_all` y `create_all`: funciona como reinicio destructivo, no como actualización de datos. |
| **Estadísticas del orientador hardcodeadas** | `OrientadorDashboardView.vue` | Se reemplazó "142 / 38 / 104" por `computed()` calculados desde `studentsPool` |
| **Nombre del orientador hardcodeado** | `OrientadorDashboardView.vue` | Se agregó `authService.getProfile()` que llama a `GET /auth/me` |
| **`authService.getProfile()` no existía** | `authService.js` | Se creó la función que llama a `GET /auth/me` |
| **Filtro de cursos hardcodeado** | `OrientadorDashboardView.vue` | Se reemplazó "4° Medio A/B/C" por un `computed` dinámico desde los datos |
| **Diagrama DER con herencia errónea** | `docs/WordBPM.docx` | Se corrigieron los 4 diagramas UML para reflejar la arquitectura real |
| **Diagrama de Casos de Uso con CU7 (PDF)** | `docs/WordBPM.docx` | Se eliminó CU7 del MVP y se movió a "Trabajo Futuro" |
| **Imagen duplicada en el .docx** | `docs/WordBPM.docx` | Se eliminó el diagrama viejo directamente desde el XML del documento |
| **Sección "Mi Historial" con múltiples intentos** | `StudentDashboardView.vue` | Se reemplazó por "Bitácora de Proceso" con timeline de eventos reales |
| **IDOR en consulta de reporte por ID** | `routers/reporte.py` | Se limita el acceso al estudiante propietario o al orientador asociado mediante curso; 404 para reportes ajenos/inexistentes y 403 para otros roles. |
| **Clave Zeebe no persistida** | `services/bpm_service.py` | Se sustituyó el atributo no mapeado `zeebe_process_instance_key` por `process_instance_key`, sin cambiar la columna ni el resto del flujo. |
| **Fecha de finalización ausente** | `routers/evaluacion.py` | Se asigna `completed_at = func.now()` junto con el estado `completada`, antes del commit. |
| **Usuarios inactivos podían autenticarse** | `services/auth_service.py`, `utils/dependencies.py` | Login rechazado y requests con tokens existentes rechazadas con 401 cuando `is_active=False`; JWT sin cambios de formato. |
| **Configuración Zeebe divergente** | `services/bpm_service.py`, `worker.py` | Ambos usan `settings.ZEEBE_GATEWAY`; se conserva `zeebe:26500` en Docker y `localhost:26500` en desarrollo local. |
| **Driver de tests no declarado** | `requirements.txt` | Se añadió `aiosqlite>=0.22.1`. |
| **Unicidad de evaluación solo en el router** | `models/evaluacion.py` | Añadida la restricción `uq_evaluacion_estudiante` para impedir varias filas por estudiante. |
| **BD existente sin la restricción UNIQUE** | `alembic/versions/20260922_unique_evaluacion_estudiante.py` | Revisión `20260922_eval_unique` aplicada y verificada en MySQL de desarrollo; 2 evaluaciones conservadas, sin duplicados. |

### Correcciones recientes verificadas en código

| Cambio | Archivos de respaldo | Resultado |
|--------|----------------------|-----------|
| Flujo orientador → reporte | `src/router/index.js`, `orientadorService.js`, `OrientadorDashboardView.vue`, `ReporteView.vue`, `routers/orientador.py` | Ruta y servicio específicos, contrato compartido y autorización por curso. |
| Identidad y resumen del reporte | `schemas/reporte.py`, `routers/reporte.py`, `routers/orientador.py`, `ReporteView.vue` | `studentName` real, iniciales, contexto por rol y resumen neutro. PDF fuera del MVP; radar y contenido neutral corregidos con el alcance de pruebas descrito en §4. |
| Resultados del dashboard estudiante | `StudentDashboardView.vue` | Datos del reporte, sin 85%/72% ni área fija; iniciales reales, sin prefijo «Prof.» añadido y fechas reales. |
| Representación BPM | `src/utils/bpmStatus.js`, tres vistas consumidoras, `schemas/orientador.py`, `routers/orientador.py` | Estado original en etiquetas, filtros y contadores; fallback neutro. |
| Recuperación y reanudación | `routers/evaluacion.py`, `evaluacionService.js`, `EvaluacionView.vue` | Nuevo GET de respuestas propias, recuperación, cola individual, reintentos, aviso de salida y espera antes del envío. |
| Bloqueo de evaluaciones terminadas | `routers/evaluacion.py`, `EvaluacionView.vue`, `test_evaluacion_respuestas.py` | Completada/procesada no editables ni reenviables; bloqueo y prueba MySQL permanente de dos envíos concurrentes. |
| Integridad del envío final | `schemas/evaluacion.py`, `routers/evaluacion.py`, `test_evaluacion_respuestas.py` | 44 entradas estrictas, IDs exactos, sin duplicados; 422 controlado y misma fuente para persistir/calcular. |
| Entrega MySQL → Zeebe | `bpm_service.py`, `models/bpm_evento.py`, `main.py`, tests BPM | Outbox antes de publicación, reintentos durables, logging JSON y workers idempotentes; probada caída real y arranque normal sin recarga. |
| Autorización de reportes | `test_reportes.py`, routers | Propiedad/curso, JWT inválidos/inactivos, inexistentes y contrato de las tres rutas. |
| Contenido vocacional | `routers/reporte.py`, tests, `ReporteView.vue` | Español, límites de inferencia, sin alto impacto fijo ni fallback a Tecnología; neutralidad ante N/empates/reglas ausentes. Matriz sin ampliar. |
| Radar y ajustes visuales | `ReporteView.vue`, `homeview.vue` | Cinco ejes por letra y cuadrícula pentagonal, también en portada. |
| Bitácora, error y fecha | `StudentDashboardView.vue`, `OrientadorDashboardView.vue` | Hash abre historial, fallo de getEstado visible con reporte y columna «Inicio de evaluación». |
| Contrato BPM antiguo | `schemas/orientador.py`, `routers/orientador.py` | Eliminados `bpmStatus/statusClass` sin consumidores; se conserva `lastUpdate`. |

Las filas históricas sobre diagramas y ediciones de `WordBPM.docx` proceden del resumen anterior; no constituyen una revalidación del documento académico en esta actualización.

### Migración de unicidad aplicada (antecedente)

- Se revisaron duplicados antes de aplicar la migración y se generó un respaldo en `/tmp/vocalis-before-eval-unique-QqYoic.sql`.
- La revisión vuelve a comprobar duplicados y aborta si los encuentra, sin borrar ni fusionar datos. No se ejecutó el seed para aplicar este cambio.
- Es la primera revisión Alembic (`down_revision = None`) y modifica el esquema existente creado por `Base.metadata.create_all`; no crea el esquema completo. No admite ejecución offline con `--sql`.
- En otras BD existentes, seguir `backend/alembic/README.md` y ejecutar `venv/bin/python -m alembic upgrade head` desde `backend`, tras revisar los datos. `create_all` no modifica tablas existentes.
- La verificación de esa etapa confirmó `uq_evaluacion_estudiante` activo y entonces `alembic_version = 20260922_eval_unique`; la revisión head actual es `20260924_bpm_outbox`, posterior a `20260922_registro_contexto`. Esto se verificó en la BD de desarrollo de este proyecto, no en otros entornos.


---

### Migración de registro aplicada

`20260922_registro_contexto` sucede a `20260922_eval_unique`: añade `orientador.establecimiento` y `estudiante.fecha_nacimiento` como nullable y crea `uq_curso_establecimiento_nombre`. Comprueba duplicados antes del DDL y aborta sin eliminarlos ni fusionarlos; requiere conexión y no ofrece downgrade destructivo automático.

Codex la probó en MySQL aislado y la aplicó en desarrollo tras respaldo (`/tmp/vocalis-before-registro-2zfq7mei.sql`). Se conservaron todas las filas, incluidos 6 usuarios, 4 estudiantes, 2 orientadores y 3 cursos, con sus asociaciones. Los nuevos campos históricos quedaron NULL. `create_all` no sustituye esta migración. La compatibilidad del seed se comprobó únicamente en una BD temporal.

**Migración posterior de entrega BPM:** `20260924_bpm_outbox` crea sólo `bpm_evento`, sin alterar evaluaciones/reportes ni inventar eventos históricos. UNIQUE evaluación/tipo y message_id; downgrade impide borrar trazabilidad automáticamente. `backend/BPM_RECOVERY.md` registra su aplicación en MySQL de desarrollo con preservación de filas y respaldo `/tmp/vocalis-before-bpm-outbox-ii1fy1j5.sql`. Tests MySQL y demo aislada verificaron además la migración. La cadena sigue necesitando bootstrap inicial.

---

## 6. Qué Queda Pendiente (Priorizado)

### Decisión funcional pendiente

1. **Asignación ambigua:** con varios orientadores del mismo establecimiento, los cursos libres quedan sin asignación. Falta definir un mecanismo de asignación autorizado. Se conservan las asociaciones existentes y los permisos por `curso.orientador_id`; compartir establecimiento no concede acceso. Los históricos desconocidos siguen NULL.

El arranque sin recarga, la validación de IDs en el guardado individual y el acceso a reportes guardados con BPM pendiente fueron corregidos y probados. Bajo 30 usuarios se reprodujeron deadlocks 1213 y conflictos 409; el guardado ahora reintenta los deadlocks de forma acotada y el registro separa bcrypt del loop y reintenta conflictos. La corrida posterior terminó sin errores; no acredita todas las intercalaciones ni mayor carga.

### Validación y entrega pendientes

- **Cobertura y pruebas:** cobertura global >80 % medida y tres pruebas permanentes del ciclo de vida Zeebe añadidas; faltan inversiones OCEAN y ventanas de caída no cubiertas. La suite MySQL incluye concurrencia, pero no demuestra todas las intercalaciones.
- **Resiliencia BPM restante:** inicios ambiguos e históricos, respuesta perdida tras aceptación remota en infraestructura real, apagones prolongados, expiración 23/24 h, pérdida de disco y múltiples réplicas no validados E2E. Recuperación breve probada; no prometer exactly-once ilimitado.
- **Responsive y navegación:** Firefox headless verificó los flujos y capturas a 1440×900 y 390×844, incluidos carga/error/reintento del panel. Se corrigieron navegación/cierre de sesión móviles, ancho del cuestionario y etiquetas del radar. Queda revisión visual humana adicional y otros navegadores/tamaños; los paneles requieren recarga para ver cambios BPM posteriores.
- **Usabilidad:** guía de cinco participantes preparada en `docs/validacion_mvp.md`; sesiones y satisfacción ≥85 % no medidas.
- **Rendimiento:** una corrida de `measure_latency.py` con 30 usuarios en la demo aislada terminó 30/30 recorridos y 1500 solicitudes sin errores; p95 de cada operación ≤1,216 s y máximo ≤1,276 s. El umbral de 3 s se cumple sólo para latencia HTTP de esa corrida local; no se midieron renderizado, finalización BPM ni variabilidad entre corridas.
- **Documentación y entrega:** guía reproducible, E2E HTTP/broker y recorrido visual automatizado disponibles. Quedan revisión académica/humana, interfaces administrativas de Compose, presentación y sesiones de usabilidad. No se acredita documentación ≥90 % ni 100 % del MVP; `v1.0-mvp` requiere autorización explícita.
- **Configuración final:** configurar privadamente `ORIENTADOR_REGISTRATION_CODE` y demás secretos; Compose conserva valores de desarrollo. La imagen Docker usada en diagnóstico estaba desactualizada respecto a aiosqlite; falta reconstruir/verificar la entrega.
- **Inicialización:** separar bootstrap, `alembic upgrade head` y seed destructivo. `create_all` no migra; el seed no administra `alembic_version` y no debe ejecutarse sobre la BD existente.
- **Reproducibilidad de reportes:** `carreras_json/interpretaciones_json` siguen sin versión ni instantánea. Acordar versión conjunta de matriz, selección, textos y política histórica antes de activarlos. `backend/REPORT_CONTENT.md` documenta la decisión y la justificación académica pendiente.

### Limpieza y elementos visuales pendientes

- **Componentes Vue reutilizables:** siguen sin extraerse sidebar, avatar, barra BPM y radar; el mapeo `bpmStatus.js` ya está compartido y no es un pendiente.
- **Mocks/orfandad:** `mockDelay.js` y `bfi44Questions.js` sin imports; `getReportById()` sin consumidor frontend; `test_login2.py` importa `pwd_context` inexistente. Scripts raíz no son la suite backend.
- **Estilos/comentarios:** tokens CSS duplicados; comentarios antiguos en `http.js`, router y ReporteView; README de plantilla. No vuelve a marcarse como pendiente la barra BPM de EvaluacionView.
- **Comentarios BPM:** `bpmStatus/statusClass` ya se retiraron del backend; el comentario de `schemas/evaluacion.py` aún enumera estados que los workers no producen.
- **Lint completo:** HomeView y authService están corregidos con lint dirigido; no se acredita lint de todo el repositorio.
- **Textos:** la landing promete personalización/compatibilidad más amplia que la implementada. El mensaje de AuthView ya indica que hay que iniciar sesión.

### Ausencias conservadas, sin convertirlas en nuevos requisitos del MVP

- **Auditoría real del orientador:** no hay visor y el botón decorativo fue retirado; no es requisito del MVP básico.
- **Paginación real:** no implementada; se muestra la lista completa y los botones decorativos fueron retirados.
- **Notificación real al orientador:** el worker solo actualiza `reporte_listo`; no hay correo ni otro canal externo. No confundir el nombre de la tarea con una notificación enviada ni incorporar mensajería como requisito nuevo.
- **Pruebas automatizadas frontend:** cuatro pruebas acotadas del reporte neutral y un recorrido Firefox headless independiente; aún faltan participantes reales y revisión humana adicional.
- **PDF y analítica predictiva:** mejoras futuras, no bugs ni requisitos de cierre; el control PDF sin función se retiró del reporte.

---

## 7. Convenciones y Patrones del Código

### Nombres de campos de modelos

| Campo | Convención | NO usar |
|-------|-----------|---------|
| Nombre completo | `nombre_completo` | `nombre`, `name`, `full_name` |
| Email | `email` | `correo`, `mail` |
| Contraseña hasheada | `hashed_password` | `password`, `pwd` |
| Rol de usuario | `rol` (RolEnum) | `role`, `tipo` |
| Estado de evaluación | `estado` (EstadoEvaluacion enum) | `status` |
| Estado BPM | `estado_actual` (string libre) | `bpm_status` |
| ID de pregunta | `pregunta_id` | `question_id` |
| Valor Likert | `valor` (1-5) | `answer`, `score` |

Los contratos HTTP tienen nombres propios: `UserProfile.name/role`, `ReporteOut.studentName`, `preguntaId`, `bpm_estado`. No deben renombrarse aplicando mecánicamente las convenciones ORM de la tabla.

### Token JWT

- Se guarda en `localStorage` con la clave **`vocalis_token`**
- Payload contiene `{ sub: email, role: "estudiante"|"orientador", exp: timestamp }`
- Header de autorización: `Authorization: Bearer <token>`
- Se decodifica en el frontend directamente (base64) en el router guard para obtener el `role`

### Estructura de carpetas del backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # BaseSettings (DATABASE_URL, ZEEBE_GATEWAY, JWT_SECRET, etc.)
│   ├── database.py        # create_async_engine, async_sessionmaker, Base, get_db, init_db
│   ├── main.py            # FastAPI, CORS, lifespan (init_db, worker y reintentos)
│   ├── seed.py            # Datos iniciales (44 preguntas, orientador, cursos, estudiante demo)
│   ├── worker.py          # Zeebe workers (calcular-ocean, generar-reporte, notificar-orientador)
│   ├── models/
│   │   ├── __init__.py    # Exporta todos los modelos
│   │   ├── usuario.py     # Usuario + RolEnum
│   │   ├── estudiante.py  # Estudiante (1:1 Usuario, N:1 Curso)
│   │   ├── orientador.py  # Orientador (1:1 Usuario, 1:N Curso)
│   │   ├── curso.py       # Curso (N:1 Orientador, 1:N Estudiante)
│   │   ├── evaluacion.py  # Evaluacion + EstadoEvaluacion enum
│   │   ├── pregunta.py    # Pregunta + DimensionEnum (O/C/E/A/N)
│   │   ├── respuesta.py   # Respuesta (check 1-5, unique evaluacion+pregunta)
│   │   ├── reporte.py     # ReporteVocacional (scores_json, carreras_json, interpretaciones_json)
│   │   ├── bpm_evento.py  # Outbox MySQL → Zeebe
│   │   └── proceso_bpm.py # ProcesoBPM (estado_actual, process_instance_key)
│   ├── routers/
│   │   ├── auth.py        # /api/auth/login, /api/auth/register, /api/auth/me
│   │   ├── evaluacion.py  # /api/evaluacion/preguntas, /respuesta, /respuestas, /enviar, /estado
│   │   ├── reporte.py     # /api/evaluacion/reporte, /reporte/{id}
│   │   └── orientador.py  # /api/orientador/estudiantes, /estudiante/{id}/reporte
│   ├── schemas/
│   │   ├── auth.py        # LoginRequest/Response, RegisterRequest/Response, UserProfile
│   │   ├── evaluacion.py  # PreguntaOut, RespuestaIn/Out, SubmitEvaluationRequest/Response, EstadoEvaluacion
│   │   ├── orientador.py  # EstudianteListItem
│   │   └── reporte.py     # DimensionScore, CareerArea, ReporteOut
│   ├── services/
│   │   ├── auth_service.py   # create_user, authenticate_user, get_user_name
│   │   ├── bpm_service.py    # Outbox, dispatch/reintentos, start_process y advance_to
│   │   └── ocean_scorer.py   # calculate_ocean_scores, get_dominant_dimensions
│   └── utils/
│       ├── security.py       # hash_password, verify_password, create_access_token, decode_access_token
│       └── dependencies.py   # get_current_user, require_estudiante, require_orientador
├── scripts/
│   ├── validate_mvp.py     # Demo HTTP/MySQL/Zeebe aislada
│   └── measure_latency.py  # Procedimiento de carga, aún sin medidas
└── tests/
    ├── conftest.py            # Fixtures: event_loop, setup_db, db_session (SQLite en memoria)
    ├── test_ocean_scorer.py   # 4 tests: neutral, extreme, invalid, 44_items_required
    ├── test_evaluacion_unique_migration.py # 3 tests de migración y unicidad
    ├── test_evaluacion_respuestas.py # 30 casos de respuestas/envío/bloqueo
    ├── test_auth_registro.py # 37 casos de registro, asignación y autorización
    ├── test_registro_migration.py # 2 tests de compatibilidad de migración
    ├── test_registro_mysql.py # 4 tests opcionales MySQL
    ├── test_bpm_delivery.py # 15 casos de outbox/reintentos
    ├── test_bpm_mysql.py # 3 tests opcionales MySQL
    ├── test_reportes.py # 53 casos de permisos/contrato/contenido
    ├── test_career_areas.py # 29 casos de reglas
    └── test_orientador_estado.py # 6 casos de estado/fecha
```

### Estructura de carpetas del frontend

```
src/
├── App.vue                    # Componente raíz (solo <RouterView />)
├── main.js                    # Montaje de Vue app + router
├── router/
│   └── index.js               # 7 rutas, incluido orientador-reporte; guards por rol
├── services/
│   ├── http.js                # Instancia Axios centralizada (baseURL, interceptor JWT, manejo 401)
│   ├── authService.js         # login, register, logout, getProfile
│   ├── evaluacionService.js   # getQuestions, getAnswers, saveAnswer, submitEvaluation, getEstado
│   ├── orientadorService.js   # getStudents, getStudentReport
│   ├── reporteService.js      # getLatestReport, getReportById
│   ├── mockDelay.js           # ⚠️ HUÉRFANO — no importado
│   └── bfi44Questions.js      # ⚠️ HUÉRFANO — no importado
├── utils/
│   └── bpmStatus.js           # Mapeo compartido de estados BPM reales
├── views/
│   ├── homeview.vue           # Landing pública
│   ├── AuthView.vue           # Login + Registro
│   ├── StudentDashboardView.vue  # Dashboard del estudiante
│   ├── EvaluacionView.vue     # Cuestionario BFI-44
│   ├── ReporteView.vue        # Reporte vocacional con radar
│   └── OrientadorDashboardView.vue  # Panel del orientador
└── components/                # ⚠️ VACÍO — sin componentes reutilizables
```

### Patrones de código a respetar

1. **Composition API con `<script setup>`** — todas las vistas usan esta sintaxis, no Options API.
2. **Servicios centralizados** — toda comunicación con el backend pasa por `src/services/`. Nunca llamar a Axios directamente desde una vista.
3. **Interceptor HTTP** — `http.js` agrega automáticamente el header `Authorization: Bearer <token>` y elimina el token si recibe un 401; no redirige desde el interceptor. El guard controla el acceso en navegaciones posteriores.
4. **Prefijo de rutas API** — todos los routers del backend se montan con `prefix="/api"`. Los endpoints completos son `/api/auth/...`, `/api/evaluacion/...`, etc.
5. **Modelos ORM con Mapped** — se usa la sintaxis `Mapped[type]` + `mapped_column()` de SQLAlchemy 2.0, no el estilo clásico `Column()`.
6. **I/O asíncrona** — routers y acceso a BD usan `async def`, `AsyncSession` y `create_async_engine`; scorer, formateadores y utilidades de seguridad son síncronos.
7. **Enums como strings** — `RolEnum`, `EstadoEvaluacion`, `DimensionEnum` heredan de `(str, enum.Enum)` para serialización directa.
8. **Scoped CSS** — cada vista tiene `<style scoped>` con sus propias variables CSS (deuda técnica conocida, debería ser global).
9. **Idioma previsto: español en UI y errores** — las descripciones OCEAN del backend ya están en español, con límites de interpretación vocacional. Los nombres de variables y funciones en el código están en inglés o spanglish (`studentName`, `nombre_completo`, `getEstado`).
10. **Nombres de archivos de vistas** — PascalCase (`StudentDashboardView.vue`), excepto `homeview.vue` (inconsistencia menor heredada).

### Endpoints API — Referencia rápida

```
POST   /api/auth/login                    → { access_token, role, name }
POST   /api/auth/register                 → { ok, message }
GET    /api/auth/me                        → { id, email, role, name }

GET    /api/evaluacion/preguntas           → [{ id, text, dimension }]
POST   /api/evaluacion/respuesta           → { preguntaId, valor, saved }
GET    /api/evaluacion/respuestas          → [{ preguntaId, valor, saved }] (solo propias)
POST   /api/evaluacion/enviar              → { reportId, status }
GET    /api/evaluacion/estado              → { tiene_evaluacion, estado, bpm_estado, fechas, orientador_nombre }
GET    /api/evaluacion/reporte             → ReporteOut
GET    /api/evaluacion/reporte/{id}        → ReporteOut

GET    /api/orientador/estudiantes         → [EstudianteListItem] (incluye bpm_estado)
GET    /api/orientador/estudiante/{id}/reporte → ReporteOut
```

`ReporteOut = { studentName, evaluatedAt, scores, dimensions, careerAreas }`. El mismo contrato se usa en las tres consultas; no incluye estado BPM. `careerAreas` puede ser `[]`; `vocationalImpact` conserva un texto neutro por compatibilidad. El radar identifica dimensiones por letra, no por orden JSON.

### Credenciales de desarrollo (seed)

| Rol | Email | Contraseña |
|-----|-------|-----------|
| Orientador | `orientador@vocalis.cl` | `vocalis123` |
| Estudiante | `estudiante@vocalis.cl` | `vocalis123` |

### Variables de entorno

```env
# Backend (config.py)
DATABASE_URL=mysql+aiomysql://vocalis:vocalis_pass@localhost:3306/vocalis_db
ZEEBE_GATEWAY=localhost:26500
JWT_SECRET=dev-secret-change-in-production
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
# Vacío deshabilita el registro de orientadores; configurar un secreto privado fuera del repositorio.
ORIENTADOR_REGISTRATION_CODE=

# Frontend (variable admitida por src/services/http.js)
VITE_API_BASE_URL=http://localhost:8000/api
```

`bpm_service.py` y `worker.py` consumen `settings.ZEEBE_GATEWAY`: `localhost:26500` en desarrollo local y `zeebe:26500` mediante la variable de entorno de Docker Compose. `ZEEBE_ADDRESS` ya no se utiliza.

### Cómo levantar el proyecto

La receta completa, secretos, bootstrap, migraciones, carga inicial no destructiva, despliegue BPMN y limpieza están en `docs/validacion_mvp.md`. No ejecutar `python -m app.seed` sobre la BD existente.

```bash
# Infraestructura de desarrollo (configurar secretos privados antes de usarla):
docker compose up -d mysql
# Seguir docs/validacion_mvp.md para crear un broker exclusivo y una BD temporal.
cd backend
source venv/bin/activate
# Configurar VOCALIS_TEST_MYSQL_ADMIN_URL en privado.
python -B scripts/validate_mvp.py --gateway 127.0.0.1:27650 \
  --zeebe-container vocalis-validation-zeebe
# Para continuar manualmente: --keep-db y seguir la guía para reiniciar el backend.
# Frontend, desde la raíz en otra terminal:
# VITE_API_BASE_URL=http://localhost:8000/api npm run dev
```

> **Configuración real:** MySQL 8 en Compose es la BD canónica, sin fallback a SQLite fuera de tests. El validador crea una BD UUID, inicializa tablas, aplica las tres revisiones, carga sólo preguntas y despliega el BPMN original. Usa un broker nuevo para evitar correlaciones entre bases con IDs repetidos. Elimina su BD salvo `--keep-db`; no altera volúmenes ajenos. La API hace `create_all`, no migra automáticamente. La demo E2E aprobada usa Uvicorn sin recarga; Compose conserva `--reload` para desarrollo. Firefox headless verificó los recorridos, y una revisión humana adicional sigue pendiente.

---

# Plan original y evolución del proyecto

El siguiente roadmap fue definido para **septiembre–noviembre de 2026** y se conserva como **referencia histórica proporcionada por el usuario**. No es un contrato técnico ni una descripción exacta de lo implementado. El código actual y sus verificaciones prevalecen sobre este plan.

### Fase 1 — Backend Foundation + MySQL

**Semanas 1–2, Sep 4–18.** FastAPI; SQLAlchemy/MySQL; modelos; Alembic; seed BFI-44; auth JWT; Docker; `ocean_scorer`; tests base.

### Fase 2 — JWT + Frontend

**Semanas 3–4, Sep 18–Oct 2.** `authService` real; localStorage; guards por rol; AuthView; `/auth/me`; tests de auth.

### Fase 3 — Camunda 8

**Semanas 5–6, Oct 2–16.** BPMN; Zeebe; workers; endpoints de evaluación; `evaluacionService`; estados BPM reales; tests BPM.

### Fase 4 — Reportes + Orientador

**Semanas 7–8, Oct 16–30.** Reportes OCEAN; recomendación vocacional; panel orientador; servicios frontend reales; consulta de reportes; tests de reporte/orientador.

### Fase 5 — Testing y validación

**Semanas 9–10, Oct 30–Nov 13.** Suite Pytest; cobertura >80%; pruebas con 5 usuarios; satisfacción ≥85%; latencia <3 s con 30 usuarios; responsive; errores de red; corrección de bugs.

### Fase 6 — Documentación y entrega

**Semanas 11–12, Nov 13–27.** WordBPM.docx; documentación técnica; Docker Compose final; release `v1.0-mvp`; presentación; demo reproducible.

### Criterios originales

- Procesos documentados ≥90%.
- Módulos funcionales: 100% del MVP.
- Satisfacción ≥85%.
- Latencia <3 s con 30 usuarios.

Son objetivos originales, **no resultados medidos**. El repositorio revisado no aporta evidencia suficiente para acreditarlos.

### Estado actual respecto al plan original — 27 de septiembre de 2026

Los estados valoran la fase completa, incluidas sus validaciones; «Parcial» no significa que todas sus tareas estén pendientes.

| Fase | Estado actual | Observaciones |
|------|---------------|---------------|
| 1 — Backend Foundation + MySQL | Implementado y probado en alcance base; cierre parcial | Diez modelos de tabla, auth, scorer, seed, MySQL y tres migraciones. Pruebas aisladas y E2E API; pregunta inexistente al guardar devuelve 422. Falta migración inicial completa y configuración final. |
| 2 — JWT + Frontend | Implementado; API y Firefox probados, cierre parcial | Servicios, JWT, guards, registro por rol, fecha/edad, curso y código privado. Registro/login/logout de ambos roles probados en Firefox a 1440×900 y 390×844; secretos finales y revisión humana adicional pendientes. |
| 3 — Camunda 8 | Implementado y probado sin recarga; resiliencia parcial | Outbox tras commit, reintentos, clave persistida, logging y estados reales; E2E MySQL/Zeebe sin `--reload` con caída/reinicio. Ventanas extremas y conciliación manual siguen pendientes. |
| 4 — Reportes + Orientador | Implementado y probado en API/Firefox; cierre parcial | Permisos por curso, tres contratos iguales, contenido neutral español, cinco ejes y reporte accesible durante incidencia BPM. 53 tests de reportes, 29 de reglas, 8 de estado y 4 de plantilla; Firefox verificó panel y reporte. Pendientes respaldo académico/versionado histórico y revisión humana adicional. |
| 5 — Testing y validación | Parcial: pruebas técnicas verificadas | 198 backend aprobadas (9 MySQL), 0 omitidas/fallidas; líneas 91,33 %, ramas 82,55 %, combinación 89,80 %. 26 checks E2E sin recarga, 4 pruebas frontend y 34 comprobaciones Firefox. Una corrida HTTP de 30 usuarios cumplió <3 s por solicitud; cinco participantes y satisfacción siguen pendientes. |
| 6 — Documentación y entrega | Parcial: guía y demo técnica/visual verificadas | Documentación de recuperación/contenido, demo HTTP/MySQL/Zeebe y recorrido Firefox reproducibles. Pendientes revisión académica/humana, despliegue final reconstruido, usabilidad y presentación. Tag v1.0-mvp no creado; requiere autorización explícita. |

### Evolución respecto del diseño inicial

- **Modelo de datos:** frente a la referencia histórica a ocho modelos, el código exporta **diez modelos de tabla** en `backend/app/models/__init__.py`, incluidos `curso` y `bpm_evento`. Roles reales: estudiante y orientador; relación estudiante → curso → orientador. La diferencia de número no es un error.
- **Recomendación:** no existe un `career_mapper.py` separado. `CAREER_MATRIX` y `get_career_areas()` están en `routers/reporte.py`; hay seis entradas explícitas, no diez. Se seleccionan referencias exploratorias al consultar scores persistidos; no hay fallback ni uso de N como inclinación profesional. La persistencia histórica versionada se aplazó.
- **Pruebas:** doce módulos backend suman 198 casos aprobados; abarcan permisos/contratos, reglas, outbox, ciclo de vida del worker y concurrencia MySQL. Hay cuatro pruebas acotadas Vue. Cobertura, E2E HTTP/Zeebe sin recarga y Firefox real medidos; quedan usabilidad y validación en otros entornos.
- **Estrategia Camunda:** el BPMN utiliza receiveTask y publicación desde la API, no un cuestionario respondido en Tasklist. La API calcula y confirma OCEAN/reporte junto con outbox antes de publicar; los workers avanzan estados idempotentes. Arranque sin recarga y recuperación breve probados, con límites de deduplicación/conciliación.
- **Avances adelantados:** al **27/09/2026**, dentro del intervalo original de fase 2, ya hay implementación de fases 3–4, pruebas/cobertura de fase 5 y guía/demo técnica de fase 6. Se conserva el calendario histórico; sólo se acredita cada resultado dentro del entorno y alcance probados, sin declarar cerrado el MVP.
