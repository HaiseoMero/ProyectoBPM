# Resumen del Proyecto — Vócalis (ProyectoBPM)

> **Propósito de este documento:** Servir como contexto completo para una herramienta de IA (Codex u otra) que retome el desarrollo del proyecto. Estado contrastado con el código al **22 de septiembre de 2026**. Se distinguen funcionalidades implementadas, límites verificados y pendientes. El plan final es una referencia histórica, no una descripción del estado actual.

---

## 1. Qué es el Proyecto

**Vócalis** es una aplicación web de orientación vocacional para estudiantes de enseñanza media en Chile. Su flujo principal es:

1. El estudiante se registra y queda asociado a un curso. El orientador se obtiene mediante ese curso cuando tiene uno asignado; los cursos sin asignación se asocian automáticamente solo cuando hay exactamente un orientador del establecimiento.
2. Completa el cuestionario psicométrico **BFI-44** (Big Five Inventory, 44 ítems con escala Likert de 5 puntos).
3. La API calcula los puntajes en las 5 dimensiones de personalidad **OCEAN** (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).
4. Se genera un **reporte vocacional** con gráfico de radar, interpretaciones textuales y carreras afines.
5. El **orientador escolar** accede a un panel de monitoreo para ver el progreso y reportes de sus estudiantes asignados.

**Camunda 8 (Zeebe)** representa el seguimiento BPM del cuestionario mediante un `receiveTask` y tres workers. El cálculo OCEAN y la creación del reporte ocurren en la API, no en Camunda. La consistencia ante fallos y la validación integral con Zeebe siguen pendientes.

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
| **Alembic** | ≥1.14 | Migraciones de BD (revisiones `20260922_eval_unique` y `20260922_registro_contexto` aplicadas en MySQL de desarrollo) |
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

**Asignación:** al registrar un estudiante se asigna su curso, si está libre, únicamente cuando existe exactamente un orientador del establecimiento. Al registrar un orientador, si es el único, se asignan los cursos libres de ese establecimiento. Con cero o varios orientadores no se elige uno arbitrariamente; las asociaciones existentes siempre se conservan. Compartir establecimiento no concede permisos: los endpoints siguen comprobando `curso.orientador_id`. El registro es atómico, usa `SERIALIZABLE` en MySQL, bloqueos y hasta tres intentos ante conflictos; la resolución de cursos ambiguos sigue pendiente.

### Registro por rol y datos históricos

- **Orientador:** requiere establecimiento y código privado `ORIENTADOR_REGISTRATION_CODE`. Sin configuración, vacío o solo espacios, devuelve 403; no hay secreto público predeterminado. Se usa `SecretStr` y `hmac.compare_digest` antes de crear el usuario. El código no se almacena ni se devuelve; los errores de validación omiten los inputs. El formulario lo solicita solo para orientadores y lo limpia tras el envío.
- **Estudiante:** requiere fecha de nacimiento ISO sin hora, establecimiento, nivel y letra. Se rechazan fechas inválidas, de hoy/futuras y edades superiores a 120 años. La edad se calcula considerando el cumpleaños. `Estudiante.edad` deriva de la fecha cuando existe; de lo contrario usa `_edad_historica`, mapeada a la columna existente `edad`. No se inventan fechas para alumnos antiguos ni se expone la fecha en `/auth/me`.
- El frontend envía campos exclusivos del rol elegido. Tras registrarse vuelve al formulario de login, sin afirmar inicio automático; JWT y redirecciones por rol se conservan.

---

### Test BFI-44 de una sola oportunidad

**Decisión:** Cada estudiante solo puede completar el cuestionario una vez. La validación del router (lógica en `evaluacion.py`) se refuerza con la restricción UNIQUE `uq_evaluacion_estudiante` sobre `evaluacion.estudiante_id`.

**Razón de diseño:** Mantener un único intento dentro del MVP simplifica la UI y la relación entre evaluación y reporte. La aplicación reutiliza la evaluación existente y rechaza edición/reenvío cuando su estado es `completada` o `procesada`; la BD garantiza una sola fila por estudiante. Esto no resuelve por sí solo las carreras entre solicitudes simultáneas (véase §6).

> **Resuelto:** El modelo declara `UniqueConstraint("estudiante_id", name="uq_evaluacion_estudiante")`. La migración Alembic `20260922_eval_unique` se aplicó después de comprobar que las 2 evaluaciones existentes no tenían duplicados; ambas se conservaron y se verificó el índice UNIQUE en MySQL.

---

### Exclusiones del MVP

| Excluido | Razón |
|----------|-------|
| **Exportación PDF** | Complejidad de renderizado server-side fuera del alcance del proyecto académico |
| **Analítica predictiva** | Requiere datos históricos masivos que no existen en un MVP |
| **Rol Administrador** | La asignación automática vía `curso` elimina la necesidad de gestión administrativa manual |
| **Tests automatizados de frontend** | Definido explícitamente como fuera del MVP en §2.6 del documento oficial |

---

### receiveTask en vez de userTask en BPMN

**Decisión:** El BPMN usa `receiveTask` (mensaje `CuestionarioCompletado`) en vez de `userTask` para la tarea del cuestionario.

**Razón:** El cuestionario se resuelve en Vue y la API publica `CuestionarioCompletado`, sin depender de una interfaz Tasklist para responder. El código actual recibe respuestas → calcula OCEAN → prepara el reporte y `completed_at` → intenta publicar el mensaje → hace commit. Los workers actualizan el seguimiento BPM. Publicar antes del commit y absorber errores de Zeebe son pendientes de consistencia; no debe describirse este recorrido como una transacción distribuida garantizada.

---

## 4. Qué se ha Implementado

### Backend — FastAPI

| Componente | Estado | Detalle |
|-----------|--------|---------|
| **Autenticación JWT** | Implementado | Login, registro y `/auth/me`. JWT HS256 con `sub`, `role`, `exp` y expiración configurable (24 h por defecto), sin cambio de formato. Login y requests rechazan `is_active=False`, incluidos tokens previamente emitidos. Registro protegido y asignación por establecimiento implementados; pruebas permanentes de registro, login/is_active y autorización por curso (§Testing). |
| **RBAC y reportes** | Implementado | `require_estudiante` y `require_orientador`; consulta por ID restringida al propietario o al orientador de sus cursos. Ajeno/inexistente: 404 en consulta por ID; otros roles: 403. La ruta específica del orientador comprueba también la pertenencia mediante curso. |
| **Cuestionario BFI-44** | Implementado con límites | Preguntas ordenadas, guardado individual y envío final. `GET /api/evaluacion/respuestas` devuelve solo respuestas de la evaluación del estudiante autenticado; devuelve lista vacía si no hay respuestas y no crea otra evaluación. Pendientes: validación exhaustiva del envío, consistencia con respuestas guardadas y concurrencia. |
| **Cálculo OCEAN** | Implementado | `ocean_scorer.py`: 16 ítems invertidos, normalización 0–1 y cinco dimensiones. Se ejecuta en `routers/evaluacion.py`. `get_dominant_dimensions()` existe, pero no tiene un consumidor efectivo en el flujo actual. |
| **Generación/consulta de reportes** | Implementado con límites | API persiste `scores_json`; `build_reporte_out()` construye `ReporteOut` con `studentName`, `evaluatedAt`, `scores`, `dimensions`, `careerAreas`. Estudiante y orientador reutilizan ese contrato. `CAREER_MATRIX` contiene seis entradas, búsqueda inversa y fallback fijo a Tecnología e Informática; las interpretaciones son genéricas. No hay `career_mapper.py` separado. |
| **Estado de evaluación** | Implementado | `GET /api/evaluacion/estado`: estado de evaluación, `bpm_estado`, fechas y orientador. `completed_at = func.now()` se asigna antes del commit al completar; no se rellenaron fechas históricas. Edición y reenvío de `completada`/`procesada` se rechazan. |
| **Panel del orientador** | Implementado con límites | Listado filtrado por cursos y reporte individual autorizado. El listado incorpora `bpm_estado` original; mantiene también campos antiguos `bpmStatus/statusClass` que todavía pueden contradecirlo. |
| **Integración Zeebe** | Parcial | Cliente y worker usan `settings.ZEEBE_GATEWAY`; se asigna y confirma `ProcesoBPM.process_instance_key` cuando el inicio es exitoso. Los workers avanzan estados; no calculan OCEAN ni envían notificaciones externas. Pendientes de recuperación ante fallos y pruebas con Zeebe real. |
| **Seed de datos** | Implementado, destructivo | 44 preguntas coherentes con dimensiones/inversiones del scorer, un orientador, tres cursos y un estudiante demo. El orientador comparte establecimiento con sus cursos; el alumno demo conserva edad histórica y fecha NULL. Compatible con el nuevo esquema, probado solo en MySQL temporal. Borra y recrea tablas del modelo; no es una migración incremental. |

### Frontend — Vue.js 3

| Vista | Estado | Detalle |
|-------|--------|---------|
| **`homeview.vue`** | Implementado | Landing pública con radar ilustrativo animado y CTA de registro. Textos de personalización y compatibilidad exceden el contrato actual; lint pendiente. |
| **`AuthView.vue`** | Implementado con límites | Login/registro por rol, establecimiento enviado, fecha de nacimiento para estudiantes y código privado para orientadores. Limpieza del código y errores comprensibles; al registrarse se solicita iniciar sesión. |
| **`StudentDashboardView.vue`** | Correcciones recientes implementadas | Eliminados 85%, 72% y área fija. Muestra `dimensions/careerAreas` del reporte real, estados neutros sin reporte y errores de carga. Nombre de `/auth/me`, iniciales dinámicas y orientador sin prefijo añadido. Bitácora con fechas de `/evaluacion/estado`, incluida `evaluacion_fecha = completed_at`; BPM desde `bpm_estado`. Sigue pendiente activar la bitácora al entrar por el hash del enlace «Mi Historial». |
| **`EvaluacionView.vue`** | Correcciones recientes implementadas | Preguntas reales, bloques de diez, recuperación de respuestas y primer bloque incompleto. Guardado individual en orden, selección local conservada ante fallos, reintento y aviso al abandonar con cambios pendientes. Envío final espera los guardados. Evaluaciones terminadas no muestran edición y ofrecen acceso al reporte. BPM mediante estado real y mapeo compartido. |
| **`ReporteView.vue`** | Correcciones recientes implementadas; radar pendiente | Distingue estudiante y orientador por ruta. Nombre real `studentName`, iniciales seguras y contexto correspondiente. Eliminados nombre/avatar/recomendación final hardcodeados; resumen neutro basado en áreas recibidas. Sin afirmación fija de finalización BPM. PDF identificado como mejora futura. Persisten errores de orden de dimensiones y geometría del radar, además de los textos genéricos recibidos del backend. |
| **`OrientadorDashboardView.vue`** | Correcciones recientes implementadas; límites pendientes | Nombre de `/auth/me`, listado real, etiquetas/filtros/contadores desde `bpm_estado`. «Ver Reporte» navega a la ruta del orientador y usa su endpoint autorizado; continúa habilitado solo en `reporte_listo`. Carga con catch/finally, error y botón Reintentar; distingue ausencia de alumnos de filtros sin resultados. «Auditar» es un alert, la paginación es visual y falta fecha real de última actualización. |

### Flujo de reportes y reanudación

- **Estudiante:** `/estudiante/reporte` → `reporteService.getLatestReport()` → `GET /api/evaluacion/reporte`.
- **Orientador:** `/orientador/estudiante/:studentId/reporte` (nombre `orientador-reporte`, guard de rol orientador) → `orientadorService.getStudentReport()` → `GET /api/orientador/estudiante/{estudiante_id}/reporte`. No utiliza una ruta exclusiva de estudiantes ni elude la autorización del backend.
- **Reporte compartido:** los endpoints anteriores y la consulta por ID usan `ReporteOut` y `build_reporte_out()`, incluido el nombre del estudiante evaluado.
- **Reanudar:** `EvaluacionView` carga preguntas, respuestas persistidas y estado antes de permitir editar. Recupera selecciones y abre el primer bloque incompleto; si todos están respondidos, abre el último. No crea una evaluación al leer.
- **Guardar/salir:** la cola mantiene las peticiones individuales en orden dentro de esa vista. Ante fallo, conserva los valores locales, marca lo pendiente y permite reintentar. La navegación espera los guardados y advierte si quedan cambios; también hay aviso `beforeunload`. Los cambios no confirmados no se convierten en un borrador persistente: si se acepta abandonarlos, pueden perderse.
- **Finalizar:** espera la cola, exige que no queden respuestas sin guardar y navega al reporte tras el envío exitoso. El servidor sigue necesitando protección transaccional frente a varias pestañas/clientes (§6).

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

### BPM / Camunda 8

| Componente | Estado verificado |
|-----------|-------------------|
| `bpmn/evaluacion-vocacional.bpmn` | Existe: receiveTask, tres serviceTasks y evento final. Su presencia no acredita despliegue vigente ni ejecución E2E. |
| Docker Compose | Configura MySQL, Zeebe, Operate, Tasklist, Elasticsearch y backend; usa `zeebe:26500`. |
| Workers Zeebe | Integrados mediante tarea en el lifespan de FastAPI. Actualizan `ProcesoBPM.estado_actual`; calcular/generar realmente ocurre en la API. |
| Mensaje `CuestionarioCompletado` | Publicación implementada; errores absorbidos y orden previo al commit pendientes de corregir. |
| Clave y configuración | `process_instance_key` correctamente mapeado; cliente/worker usan `settings.ZEEBE_GATEWAY` (`localhost:26500` local). `ZEEBE_ADDRESS` no es configuración efectiva. |

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
| `backend/tests/conftest.py` | Fixtures básicas de SQLite; la nueva suite de respuestas define su propia fixture asíncrona y cliente HTTP. |
| `backend/tests/test_ocean_scorer.py` | 4 tests: neutral, extremo parcial de Extraversión, valor inválido y cantidad incompleta. No cobertura exhaustiva de cada inversión/dimensión. |
| `backend/tests/test_evaluacion_unique_migration.py` | 3 tests: preservación y unicidad/downgrade, aborto ante duplicados y restricción ya existente. |
| `backend/tests/test_evaluacion_respuestas.py` | 30 casos contando parametrizaciones: aislamiento, recuperación, guardado, bloqueo de evaluaciones terminadas, validación del envío final, persistencia coherente y rollback. FastAPI/httpx con SQLite en memoria. |
| `backend/tests/__init__.py` | Inicialización del paquete; no añade tests. |
| `backend/tests/test_auth_registro.py` | 37 casos: registro por rol/código, fechas/edad, login e is_active, cursos por establecimiento, cero/uno/varios orientadores, conservación de asociaciones, autorización por curso y rollback. |
| `backend/tests/test_registro_migration.py` | 2 tests: preservación de datos/NULL/unicidad y aborto ante duplicados. |
| `backend/tests/test_registro_mysql.py` | 4 tests opcionales: registros simultáneos de estudiantes; estudiante/orientador concurrentes; migración con datos antiguos y UNIQUE; seed compatible. Crean y eliminan solo bases temporales propias. |
| Auth completo, reportes/orientador y Zeebe | Las pruebas anteriores no cubren íntegramente todos los flujos de autenticación y reportes ni la integración con Zeebe. |
| E2E con Zeebe real | Sin pruebas automatizadas verificadas. |
| Tests automatizados frontend | No implementados; excluidos del MVP actual. |

**Resultados diferenciados (22/09/2026):** `reporte_revision_codex.md`, revisión independiente de Antigravity, informa **76 aprobadas y 4 omitidas**. Las omitidas requieren `VOCALIS_TEST_MYSQL_ADMIN_URL`; no son fallos ni acreditan ejecución MySQL en esa revisión. En la implementación previa, **Codex ejecutó las 80 pruebas satisfactoriamente**, incluidas las cuatro sobre bases aisladas de MySQL 8.0.46. No se repitieron tests para esta actualización documental. `aiosqlite>=0.22.1` está declarado; no se ha medido cobertura global ni acreditado >80%.

**Comprobaciones auxiliares:** Codex verificó la migración aplicada y la conservación de todas las filas en MySQL de desarrollo; no ejecutó allí el seed. Build, ESLint dirigido a los tres archivos frontend modificados y `git diff --check` pasaron durante la implementación. Los errores anteriores de lint en `authService.js` se corrigieron; el hallazgo previo de `homeview.vue` sigue pendiente y no se repitió el lint completo. Estas comprobaciones y la revisión de Antigravity no equivalen a validación E2E con Zeebe.


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
| Identidad y resumen del reporte | `schemas/reporte.py`, `routers/reporte.py`, `routers/orientador.py`, `ReporteView.vue` | `studentName` real, iniciales, contexto por rol y resumen neutro. PDF fuera del MVP; quedan pendientes de radar y contenido backend (§6). |
| Resultados del dashboard estudiante | `StudentDashboardView.vue` | Datos del reporte, sin 85%/72% ni área fija; iniciales reales, sin prefijo «Prof.» añadido y fechas reales. |
| Representación BPM | `src/utils/bpmStatus.js`, tres vistas consumidoras, `schemas/orientador.py`, `routers/orientador.py` | Estado original en etiquetas, filtros y contadores; fallback neutro. |
| Recuperación y reanudación | `routers/evaluacion.py`, `evaluacionService.js`, `EvaluacionView.vue` | Nuevo GET de respuestas propias, recuperación, cola individual, reintentos, aviso de salida y espera antes del envío. |
| Bloqueo de evaluaciones terminadas | `routers/evaluacion.py`, `EvaluacionView.vue`, `test_evaluacion_respuestas.py` | Completada/procesada no editables ni reenviables en recorrido secuencial; concurrencia pendiente. |

Las filas históricas sobre diagramas y ediciones de `WordBPM.docx` proceden del resumen anterior; no constituyen una revalidación del documento académico en esta actualización.

### Migración de unicidad aplicada (antecedente)

- Se revisaron duplicados antes de aplicar la migración y se generó un respaldo en `/tmp/vocalis-before-eval-unique-QqYoic.sql`.
- La revisión vuelve a comprobar duplicados y aborta si los encuentra, sin borrar ni fusionar datos. No se ejecutó el seed para aplicar este cambio.
- Es la primera revisión Alembic (`down_revision = None`) y modifica el esquema existente creado por `Base.metadata.create_all`; no crea el esquema completo. No admite ejecución offline con `--sql`.
- En otras BD existentes, seguir `backend/alembic/README.md` y ejecutar `venv/bin/python -m alembic upgrade head` desde `backend`, tras revisar los datos. `create_all` no modifica tablas existentes.
- La verificación de esa etapa confirmó `uq_evaluacion_estudiante` activo y entonces `alembic_version = 20260922_eval_unique`; la revisión actual es `20260922_registro_contexto`. Esto se verificó en la BD de desarrollo de este proyecto, no en otros entornos.


---

### Migración de registro aplicada

`20260922_registro_contexto` sucede a `20260922_eval_unique`: añade `orientador.establecimiento` y `estudiante.fecha_nacimiento` como nullable y crea `uq_curso_establecimiento_nombre`. Comprueba duplicados antes del DDL y aborta sin eliminarlos ni fusionarlos; requiere conexión y no ofrece downgrade destructivo automático.

Codex la probó en MySQL aislado y la aplicó en desarrollo tras respaldo (`/tmp/vocalis-before-registro-2zfq7mei.sql`). Se conservaron todas las filas, incluidos 6 usuarios, 4 estudiantes, 2 orientadores y 3 cursos, con sus asociaciones. Los nuevos campos históricos quedaron NULL. `create_all` no sustituye esta migración. La compatibilidad del seed se comprobó únicamente en una BD temporal.

---

## 6. Qué Queda Pendiente (Priorizado)

### Bugs funcionales y de integridad confirmados

1. **Radar del reporte:** `ReporteView.vue` etiqueta posiciones O,C,E,A,N, mientras `build_reporte_out()` conserva el orden del JSON. MySQL devolvió A,C,E,N,O en la auditoría; además hay seis ejes estáticos frente a cinco dimensiones. Corregir correspondencia por letra y geometría.
2. **Consistencia del envío:** `routers/evaluacion.py` calcula desde el payload final sin actualizar/contrastar `Respuesta`. Puede generar un reporte que no corresponde a las respuestas persistidas.
3. **Concurrencia:** guardar/completar comprueba estado antes de escribir sin bloqueo de filas. UNIQUE protege una evaluación/reporte, pero no evita respuestas tardías, errores de integridad ni mensajes BPM duplicados. La cola Vue no coordina otras pestañas/clientes.
4. **Asignación ambigua (límite de diseño):** con varios orientadores los cursos libres permanecen sin asignación; falta un mecanismo explícito de resolución. No reasignar los cursos existentes ni ampliar permisos por establecimiento. Los errores de registro, unicidad, establecimiento descartado y edad fija están corregidos; los datos institucionales históricos desconocidos siguen NULL.
5. **Consistencia Zeebe:** errores de inicio/publicación absorbidos, mensaje previo al commit y ausencia de recuperación controlada. Puede existir reporte con proceso atascado o avance BPM sin reporte confirmado.
6. **Disponibilidad de reportes en panel orientador:** botón condicionado a `reporte_listo` aunque la API ya haya generado un reporte. Resolver sin eludir autorización.
7. **Validación de respuestas:** IDs repetidos o fuera de rango en un payload de longitud 44 producen ValueError/HTTP 500. `preg_map` no se utiliza; falta validar conjunto de preguntas y existencia al guardar.
8. **Contenido vocacional backend:** fallback fijo a Tecnología e Informática y «Alto impacto en áreas relacionadas» para cualquier puntaje. Sustituir afirmaciones no respaldadas por contenido neutro, sin inventar otra lógica vocacional.
9. **Panel orientador:** «Última Actualización» usa `evaluacion.created_at`, no una fecha real de actualización. Carga, errores, estado vacío y reintento ya están resueltos.
10. **Navegación de bitácora:** «Mi Historial» desde ReporteView añade hash, pero StudentDashboardView mantiene la pestaña dashboard y no muestra la sección.

### Validación y entrega pendientes

- **Cobertura backend amplia:** 80 casos (76 aprobados y 4 omitidos en Antigravity; 80 aprobados por Codex con MySQL aislado) no acreditan cobertura >80%. Ya hay pruebas de registro/login/is_active, permisos por curso, envío final y concurrencia de registro; quedan cobertura integral de auth/reportes, concurrencia del flujo de evaluación, matriz/radar y validación E2E con Zeebe real.
- **Responsive y usabilidad:** existen reglas CSS responsive, pero no hay evidencia de validación completa de las vistas. No confundir CSS presente con pruebas realizadas.
- **Pruebas con usuarios:** no hay evidencia verificada de cinco participantes ni satisfacción ≥85%.
- **Rendimiento:** no hay benchmark verificado de latencia <3 s con 30 usuarios.
- **Documentación académica/técnica, demo reproducible y entrega:** documentos y Compose existen, pero su presencia no acredita cierre, procesos documentados ≥90%, cumplimiento funcional del 100% del MVP ni release `v1.0-mvp`.
- **Configuración final:** configurar privadamente `ORIENTADOR_REGISTRATION_CODE` en cada entorno antes de habilitar nuevos orientadores y completar las instrucciones de despliegue. `.env.example` lo deja vacío e incluye un ejemplo no utilizable; nunca versionar el secreto. Los secretos y puertos de Compose siguen siendo de desarrollo; no presentar esta configuración como preparada para exposición pública.
- **Inicialización/migraciones:** `create_all` no migra BD existentes; el seed borra tablas y no administra `alembic_version`. Mantener instrucciones que distingan instalación, migración y reinicio de datos.
- **Supervisión BPM:** health check de API no acredita salud del worker ni despliegue del BPMN.
- **Reproducibilidad de reportes:** carreras/interpretaciones se recalculan al consultar; los campos `carreras_json/interpretaciones_json` no se rellenan en el envío.

### Limpieza y elementos visuales pendientes

- **Componentes Vue reutilizables:** siguen sin extraerse sidebar, avatar, barra BPM y radar; el mapeo `bpmStatus.js` ya está compartido y no es un pendiente.
- **Mocks/orfandad:** `mockDelay.js` y `bfi44Questions.js` sin imports; `getReportById()` sin consumidor frontend; `test_login2.py` importa `pwd_context` inexistente. Scripts raíz no son la suite backend.
- **Estilos/comentarios:** tokens CSS duplicados; comentarios antiguos en `http.js`, router y ReporteView; README de plantilla. No vuelve a marcarse como pendiente la barra BPM de EvaluacionView.
- **Contrato BPM heredado:** `bpmStatus/statusClass` aún pueden contradecir `bpm_estado`; el comentario del schema enumera estados que los workers no producen.
- **Lint completo:** queda el hallazgo previo sobre el nombre de componente `homeview`; los errores de `authService.js` se corrigieron y su lint dirigido pasó.
- **Textos:** la landing promete personalización/compatibilidad más amplia que la implementada. El mensaje de AuthView ya indica que hay que iniciar sesión.

### Ausencias conservadas, sin convertirlas en nuevos requisitos del MVP

- **Auditoría real del orientador:** «Auditar» solo ejecuta un alert. No hay visor; el alcance básico exige listado y consulta de resultados. Ocultar o identificar el placeholder sin ampliar el MVP.
- **Paginación real:** no implementada; se muestra la lista completa y los botones son decorativos.
- **Notificación real al orientador:** el worker solo actualiza `reporte_listo`; no hay correo ni otro canal externo. No confundir el nombre de la tarea con una notificación enviada ni incorporar mensajería como requisito nuevo.
- **Pruebas automatizadas frontend:** siguen sin implementarse y fuera del MVP por decisión actual; la validación manual continúa pendiente.
- **PDF y analítica predictiva:** mejoras futuras, no bugs ni requisitos de cierre.

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
│   ├── main.py            # FastAPI app, CORS, lifespan (init_db + start_worker), router mounts
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
│   │   ├── bpm_service.py    # start_process, advance_to, finish_cuestionario
│   │   └── ocean_scorer.py   # calculate_ocean_scores, get_dominant_dimensions
│   └── utils/
│       ├── security.py       # hash_password, verify_password, create_access_token, decode_access_token
│       └── dependencies.py   # get_current_user, require_estudiante, require_orientador
└── tests/
    ├── conftest.py            # Fixtures: event_loop, setup_db, db_session (SQLite en memoria)
    ├── test_ocean_scorer.py   # 4 tests: neutral, extreme, invalid, 44_items_required
    ├── test_evaluacion_unique_migration.py # 3 tests de migración y unicidad
    ├── test_evaluacion_respuestas.py # 30 casos de respuestas/envío/bloqueo
    ├── test_auth_registro.py # 37 casos de registro, asignación y autorización
    ├── test_registro_migration.py # 2 tests de compatibilidad de migración
    └── test_registro_mysql.py # 4 tests opcionales en MySQL aislado
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
9. **Idioma previsto: español en UI y errores** — las interpretaciones de dimensiones del backend aún contienen texto en inglés. Los nombres de variables y funciones en el código están en inglés o spanglish (`studentName`, `nombre_completo`, `getEstado`).
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

`ReporteOut = { studentName, evaluatedAt, scores, dimensions, careerAreas }`. El mismo contrato se usa en las tres consultas de reportes; no incluye estado BPM.

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

```bash
# 1. Infraestructura (MySQL, Zeebe, Operate, Tasklist, Elasticsearch)
docker-compose up -d

# 2. Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m app.seed          # SOLO reinicio demo: borra tablas y datos existentes
uvicorn app.main:app --reload --port 8000

# 3. Frontend, desde la raíz del repositorio (otra terminal)
npm install
npm run dev                  # http://localhost:5173
```

> **Configuración real:** MySQL 8 mediante Docker Compose es la BD de desarrollo canónica. `database.py` usa `settings.DATABASE_URL` y no implementa fallback automático a SQLite. SQLite en memoria se usa en tests. Para actualizar BD existentes se sigue `backend/alembic/README.md`, sin ejecutar el seed. El arranque del backend hace `create_all`, no `alembic upgrade head`. El despliegue del BPMN y el recorrido real por Zeebe deben verificarse aparte; los comandos anteriores no acreditan una demo E2E.


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

### Estado actual respecto al plan original — 22 de septiembre de 2026

Los estados valoran la fase completa, incluidas sus validaciones; «Parcial» no significa que todas sus tareas estén pendientes.

| Fase | Estado actual | Observaciones |
|------|---------------|---------------|
| 1 — Backend Foundation + MySQL | Parcial | FastAPI, nueve modelos, MySQL/Compose, scorer, seed, JWT y tests base existen. UNIQUE y revisión Alembic verificados en MySQL de desarrollo. El bootstrap sigue dependiendo de create_all; registro/asignación corregidos con migración de contexto aplicada; persisten ambigüedad entre varios orientadores y pendientes de validación/consistencia del flujo BPM. |
| 2 — JWT + Frontend | Parcial | authService, localStorage, guards, AuthView y /auth/me implementados; is_active verificado. Registro por rol, fecha/edad y establecimiento implementados, con pruebas permanentes; configuración privada del código y cobertura integral de auth pendientes. |
| 3 — Camunda 8 | Parcial | BPMN, cliente, workers, endpoints y mapeo real frontend implementados. La API calcula OCEAN; workers hacen seguimiento. No hay tests BPM con Zeebe real ni garantía ante fallos de publicación/commit. |
| 4 — Reportes + Orientador | Parcial | Servicios y consultas por rol operativas en código; ReporteOut compartido, identidad real y autorización por curso. Carga/error/reintento del panel resueltos. Pendientes radar, fallback vocacional, fecha real de actualización y tests completos de reportes/orientador. |
| 5 — Testing y validación | Parcial | 76 aprobadas y 4 omitidas en Antigravity; Codex verificó 80 aprobadas con MySQL aislado. Manejo de errores y reanudación en cuestionario, CSS responsive presente. Sin cobertura >80% medida, validación responsive completa, cinco usuarios, satisfacción acreditada ni benchmark de 30 usuarios. |
| 6 — Documentación y entrega | Parcial | Documentos académicos/técnicos y Compose existen; este resumen se actualiza. Persisten descripciones académicas por contrastar. Sin evidencia verificada de presentación final, demo E2E reproducible o release v1.0-mvp; no hay tag local con ese nombre. |

### Evolución respecto del diseño inicial

- **Modelo de datos:** frente a la referencia histórica a ocho modelos, el código actual exporta **nueve** en `backend/app/models/__init__.py`, incluido `curso`. Roles reales: estudiante y orientador; relación estudiante → curso → orientador. La diferencia de número no es un error.
- **Recomendación:** no existe un `career_mapper.py` separado. `CAREER_MATRIX` y `get_career_areas()` están en `routers/reporte.py`; hay seis entradas explícitas, no diez. Se calcula al consultar a partir de scores persistidos.
- **Pruebas:** a `test_ocean_scorer.py`, `test_evaluacion_unique_migration.py` y `test_evaluacion_respuestas.py` se suman `test_auth_registro.py`, `test_registro_migration.py` y `test_registro_mysql.py`. Registro y permisos por curso tienen pruebas reales; cobertura integral de auth/reportes y E2E con Zeebe siguen pendientes.
- **Estrategia Camunda:** el BPMN utiliza receiveTask y publicación desde la API, no un cuestionario respondido en Tasklist. La API calcula OCEAN y prepara el reporte; los workers avanzan estados. Esto documenta la evolución arquitectónica, sin dar por resueltos los fallos transaccionales señalados en §6.
- **Avances adelantados:** al **22/09/2026**, durante el intervalo original de la fase 2, ya existen partes importantes de las fases 3 y 4 (integración, estados, reportes y panel) y tests/correcciones de fase 5. Haber adelantado código no significa haber completado sus pruebas o criterios de aceptación.
