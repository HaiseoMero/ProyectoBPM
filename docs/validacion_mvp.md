# Validación integral del MVP de Vócalis

Fecha: 27 de septiembre de 2026. Fuente de verdad: código y ejecuciones locales en MySQL 8.0.46, Zeebe 8.6.7, Python 3.14.7 y Firefox 156.0.1. No se creó ningún tag.

## Resultado y alcance

**El recorrido estudiante → BFI-44 → reporte → orientador y la recuperación ante caída de Zeebe pasaron con Uvicorn normal, sin `--reload`.** Se ejecutó un navegador real en escritorio y móvil. Las sesiones de usabilidad con personas y la validación en un despliegue de producción siguen pendientes.

| Verificación | Resultado | Evidencia/alcance |
|---|---|---|
| Suite backend completa | **198 aprobadas, 0 omitidas, 0 fallidas** | Incluidas nueve pruebas MySQL opcionales: cinco de registro/migración/seed y cuatro de BPM/concurrencia |
| Frontend existente | 4 aprobadas | `node --test tests/frontend/reporte-neutral.test.mjs`; pruebas de plantilla |
| Compilación y calidad frontend | Aprobadas | `npm run build`, ESLint dirigido a las cuatro vistas modificadas y `git diff --check` |
| Instalación aislada MySQL | Aprobada | BD UUID nueva, `Base.metadata.create_all` y tres migraciones Alembic hasta `20260924_bpm_outbox`; solo 44 preguntas cargadas, sin seed destructivo |
| E2E API/MySQL/Zeebe sin `--reload` | **26/26 comprobaciones** | Registro de ambos roles, curso, parcial/reanudación, 44 respuestas, envío, reporte, autorización por curso, BPMN real y `reporte_listo` |
| Caída y recuperación de Zeebe | Aprobada | Reporte conservado y accesible con BPM pendiente; reinicio del mismo broker, reintento de outbox y avance a `reporte_listo` |
| Navegador real | **34 verificaciones funcionales y 3 de error/reintento** | Firefox headless, build de Vue, 1440×900 y 390×844; rutas y capturas abajo |
| Carga local de 30 usuarios | **30/30 recorridos; 1500 solicitudes; 0 errores** | Una corrida, p95 máximo por operación 1,216 s; criterio <3 s **por petición HTTP**, no por recorrido ni renderizado |
| Usabilidad con cinco participantes | Pendiente | Pauta preparada; no hay resultados de personas reales |

### Arranque del worker y límite de la prueba

El fallo histórico sin recarga se debía a crear el canal gRPC al importar `app/worker.py`, antes del event loop definitivo. El código actual crea el canal, cliente y worker dentro del lifespan activo; cierra las referencias al apagar y hace observables los fallos de tareas. Tres tests de ciclo de vida cubren esta conducta. La prueba integrada inició `uvicorn app.main:app` sin recarga, desplegó el BPMN y observó jobs reales hasta `reporte_listo`, también después de reiniciar el broker. No se ha certificado una imagen backend reconstruida ni un despliegue con múltiples réplicas.

### Recuperación y límites

Se verificó una caída real después de iniciar la instancia y antes de publicar el cuestionario. El reporte quedó confirmado, la consulta devolvió 200 y `bpm_evento` quedó `pendiente` con `ZeebeGatewayUnavailableError`. Tras reiniciar el mismo broker, el proceso de reintento publicó el evento sin repetir el envío HTTP del estudiante. Las trazas del broker permiten distinguir publicación, correlación y ejecución de jobs. En la demo final se comprobaron dos publicaciones y seis jobs completados (los tres tipos por cada instancia), deduplicando los registros del exporter por partición y posición para no contar de nuevo los reproducidos durante el reinicio.

Las pruebas automatizadas adicionales cubren fallo de commit, fallo de publicación, reintentos, solicitudes repetidas y competencia de sesiones MySQL. No equivalen a una prueba de todas las ventanas de caída posibles. Siguen fuera de la evidencia de esta ejecución: caída justo después de aceptación remota antes del commit local, apagones prolongados, expiración de 23/24 horas, conciliación de inicios `incierto`, pérdida de disco y múltiples réplicas backend. Véase `backend/BPM_RECOVERY.md`. No se afirma una garantía distribuida de exactly-once.

Los paneles consumen el estado al cargar la vista (`StudentDashboardView.vue:219`, `OrientadorDashboardView.vue:233`); no hay sondeo continuo. Para la demo se debe recargar/volver a entrar. Los estados intermedios pueden transcurrir entre dos lecturas. `src/utils/bpmStatus.js` traduce `registro`, `calculando_ocean`, `generando_reporte`, `reporte_listo`; null/desconocido se muestra neutral. No se insertaron estados artificiales en MySQL para simular el avance.

## Cobertura backend medida

Medición con coverage.py 7.16.1, `--branch --source=app`, sobre todo `backend/app`; tests, migraciones y validador externo no entran en el denominador.

| Métrica | Resultado |
|---|---|
| Líneas ejecutadas | **917 / 1004 = 91,33 %** |
| Ramas ejecutadas | **175 / 212 = 82,55 %** |
| Combinación líneas + ramas de coverage.py | **89,80 %** |

Las 198 pruebas son un conteo, no un porcentaje de cobertura. `main.py` alcanzó 96 % y `worker.py` 44 % en pytest; el avance real de Zeebe se comprobó aparte. Sin `VOCALIS_TEST_MYSQL_ADMIN_URL` se omiten **nueve** pruebas MySQL y no deben contarse como aprobadas. Los fixtures crean y eliminan sólo sus bases UUID temporales; el seed destructivo se invoca únicamente en una de esas bases aisladas.

Reproducción desde `backend/`, con un entorno virtual activo y la URL administrativa del laboratorio configurada de forma privada:

```bash
export PYTHONDONTWRITEBYTECODE=1
export COVERAGE_FILE=/tmp/vocalis-mvp.coverage
python -B -m coverage run --branch --source=app -m pytest tests -q -ra -p no:cacheprovider
python -B -m coverage report
python -B -m coverage json -o /tmp/vocalis-coverage.json
```

## Demo reproducible desde cero

### 1. Dependencias y aislamiento

Requiere Docker, Python con las dependencias de `backend/requirements.txt`, Node compatible con `package.json`, y los paquetes frontend instalados. No es necesario Operate/Tasklist/Elasticsearch para ejecutar el proceso con Zeebe: esta demo comprueba el broker mediante gRPC y los estados mediante API/BD. Las interfaces administrativas completas de Compose quedan como comprobación manual adicional.

```bash
# Desde la raíz del repositorio. Usar un virtualenv propio del laboratorio.
python -m venv /tmp/vocalis-validation-venv
. /tmp/vocalis-validation-venv/bin/activate
python -m pip install -r backend/requirements.txt
npm ci
```

Para usar MySQL canónico ya existente: `docker compose up -d mysql` (o `docker-compose up -d mysql`). Configurar `VOCALIS_TEST_MYSQL_ADMIN_URL` mediante una entrada privada, apuntando a `mysql`, con permisos para crear/borrar bases temporales. El validador **no usa `vocalis_db` como destino**, no llama al seed y no modifica sus tablas. No cambiar las credenciales de un volumen ya inicializado mediante variables de arranque.

Para un laboratorio completamente nuevo, con secreto y volumen propios:

```bash
export DEMO_SUFFIX="$(python -c 'import uuid; print(uuid.uuid4().hex[:12])')"
export DEMO_MYSQL="vocalis-demo-mysql-$DEMO_SUFFIX"
export DEMO_MYSQL_VOLUME="vocalis-demo-mysql-data-$DEMO_SUFFIX"
export MYSQL_ROOT_PASSWORD="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
docker volume create --label vocalis.validation=true "$DEMO_MYSQL_VOLUME"
docker run -d --name "$DEMO_MYSQL" --label vocalis.validation=true \
  -p 127.0.0.1:23306:3306 --env MYSQL_ROOT_PASSWORD \
  --mount "type=volume,source=$DEMO_MYSQL_VOLUME,target=/var/lib/mysql" mysql:8.0
# Esperar a que MySQL responda; no continuar sólo porque el contenedor existe.
docker exec "$DEMO_MYSQL" sh -c 'MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysqladmin ping -uroot --silent'
export VOCALIS_TEST_MYSQL_ADMIN_URL="$(python -c 'import os; from sqlalchemy.engine import URL; print(URL.create("mysql+aiomysql", username="root", password=os.environ["MYSQL_ROOT_PASSWORD"], host="127.0.0.1", port=23306, database="mysql").render_as_string(hide_password=False))')"
```

No imprimir la URL ni guardar secretos en Git. El uso del administrador como usuario de aplicación se limita a este laboratorio aislado. Para un despliegue real corresponde un usuario limitado a su base.

### 2. Broker nuevo y exclusivo

No compartir broker entre bases distintas con IDs de evaluación repetidos: la correlación actual usa `evaluacion_id`. Crear un broker **nuevo para cada ejecución desde cero**; no conectar esta validación al broker de una demo ajena.

```bash
docker run -d --name vocalis-validation-zeebe --label vocalis.validation=true \
  --memory=2g -p 127.0.0.1:27650:26500 \
  -e JAVA_TOOL_OPTIONS='-Xms512m -Xmx512m' \
  -e ZEEBE_BROKER_DATA_DISKUSAGECOMMANDWATERMARK=0.998 \
  -e ZEEBE_BROKER_DATA_DISKUSAGEREPLICATIONWATERMARK=0.999 \
  -e ZEEBE_BROKER_EXPORTERS_DEBUG_CLASSNAME=io.camunda.zeebe.broker.exporter.debug.DebugLogExporter \
  -e ZEEBE_BROKER_EXPORTERS_DEBUG_ARGS_LOGLEVEL=INFO camunda/zeebe:8.6.7
```

Los límites de disco siguen la configuración de desarrollo existente; reservar espacio libre suficiente. El exporter de diagnóstico escribe datos sintéticos en logs y sólo se usa en este laboratorio. Si el nombre/puerto ya existe, detenerse y determinar su propietario; no borrar un contenedor por coincidencia de nombre.

### 3. Inicialización, migraciones, secretos y despliegue BPMN

```bash
cd backend
python -B scripts/validate_mvp.py \
  --gateway 127.0.0.1:27650 --zeebe-container vocalis-validation-zeebe
```

El script:

1. Crea `vocalis_demo_<uuid>`; no acepta una BD existente como destino.
2. Inicializa `Base.metadata.create_all` porque las revisiones existentes no constituyen una migración inicial completa; ejecuta después `alembic upgrade head`. Las revisiones son `20260922_eval_unique` → `20260922_registro_contexto` → `20260924_bpm_outbox`.
3. Inserta sólo las 44 preguntas desde `app.seed.PREGUNTAS`, con IDs/orden 1–44, sin llamar a `seed_data()` ni borrar tablas.
4. Genera `JWT_SECRET` y `ORIENTADOR_REGISTRATION_CODE` aleatorios. Exporta explícitamente `DATABASE_URL` y `ZEEBE_GATEWAY` al servidor. El código privado se entrega sólo al registro de orientadores, nunca mediante `VITE_*`.
5. Espera la topología y despliega el BPMN original mediante `ZeebeClient.deploy_resource`. No basta con copiar el archivo al contenedor. En pyzeebe instalado el método es `deploy_resource`, no `deploy_process`.
6. Inicia Uvicorn en un puerto libre y ejecuta los recorridos HTTP. Detiene/reinicia únicamente el contenedor con etiqueta `vocalis.validation=true` y puerto coincidente.
7. Escribe `checks.json`, logs, revisión, topología, despliegue y estados de outbox en `/tmp/vocalis-demo-*`. `environment.json` es privado (0600, directorio 0700); contiene secretos y no debe publicarse.
8. Detiene Uvicorn y elimina sólo su BD nueva. No elimina automáticamente el broker, para permitir recoger evidencias. Un check fallido devuelve exit code 1.

El comando anterior usa Uvicorn normal, sin `--reload`. `--diagnose-worker` conserva utilidad diagnóstica, pero no se requiere para acreditar el avance actual.

### 4. Continuar la demo manual en Vue

Añadir `--keep-db` para conservar únicamente la base nueva. Al terminar el script el servidor se detiene. Tomar el directorio `ARTIFACTS` que imprime, arrancar de nuevo contra esa misma base y el **mismo broker**:

```bash
# Desde backend, con el virtualenv activo. Reemplazar la ruta por la de esa ejecución.
export VOCALIS_DEMO_ARTIFACTS=/tmp/vocalis-demo_REEMPLAZAR
python -B - <<'PY'
import json, os, subprocess, sys
from pathlib import Path
folder = Path(os.environ['VOCALIS_DEMO_ARTIFACTS'])
env = dict(os.environ, **json.loads((folder / 'environment.json').read_text()))
subprocess.run([sys.executable, '-B', '-m', 'uvicorn', 'app.main:app',
                '--host', '127.0.0.1', '--port', '8000'], env=env, check=True)
PY
```

En otra terminal, desde la raíz:

```bash
VITE_API_BASE_URL=http://localhost:8000/api npm run dev -- --host 127.0.0.1
```

Abrir `http://localhost:5173` (permitido por CORS). Las cuentas sintéticas y contraseña generada están en `accounts.json` privado. El alumno del recorrido automatizado ya está completado; registrar otro para demostrar guardado/reanudación. Usar establecimiento `Demo`, `4° Medio A` para asociarlo al orientador ya creado. Leer el código privado del archivo privado sólo si se necesita otro orientador.

Pauta manual de aceptación:

- Registrar ambos roles; sin código correcto el orientador debe ser rechazado. Comprobar el curso y que un orientador ajeno no acceda.
- Responder parcialmente, salir tras confirmar guardados, volver a iniciar sesión y continuar con selecciones recuperadas. Verificar 44 respuestas, un solo intento y edición bloqueada tras finalizar.
- Ver los cinco puntajes y etiquetas del radar, ausencia de recomendación inventada cuando las reglas no cubren el caso, nombre correcto y mismo reporte desde ambos roles.
- Recargar ambos paneles después de la finalización y comprobar `Reporte disponible`. No prometer actualización automática ni permanencia visible de fases instantáneas.
- Comprobar «Mi Historial», fechas reales, errores de conexión y reintentos; comprobar que no se ofrece exportación PDF dentro del MVP.
- Registrar navegador/versión, capturas con datos sintéticos, pasos, resultado esperado/obtenido y cualquier incidencia. Repetir con personas en revisión visual/uso real; la automatización no sustituye esa observación.

### 5. Cierre seguro del laboratorio

Archivar sólo evidencia sin secretos. Verificar propietario y etiqueta antes de limpiar. El validador elimina su BD salvo `--keep-db`; si se conserva, tomar el nombre exacto de `runtime.json` y eliminar **sólo esa BD** después de terminar la demo. No usar comodines, `docker volume prune` ni `docker compose down -v` sobre el proyecto existente.

```bash
# Sólo los recursos que se crearon con los comandos de esta guía.
docker inspect vocalis-validation-zeebe --format '{{ index .Config.Labels "vocalis.validation" }}'
docker rm -f vocalis-validation-zeebe
# Si se creó el MySQL aislado de esta guía, y una vez terminadas todas las pruebas:
docker rm -f "$DEMO_MYSQL"
docker volume rm "$DEMO_MYSQL_VOLUME"
unset MYSQL_ROOT_PASSWORD VOCALIS_TEST_MYSQL_ADMIN_URL
```

## Procedimiento de latencia: 30 usuarios concurrentes

Se ejecutó `backend/scripts/measure_latency.py` contra la API del laboratorio aislado después de corregir bloqueos de MySQL reproducidos en la primera corrida. El destino debe ser siempre una BD aislada.

```bash
# Desde backend con la API y Zeebe del laboratorio disponibles.
python -B scripts/measure_latency.py --base-url http://127.0.0.1:8000 \
  --isolated-demo --users 30 --think-seconds 0 --timeout 30 --deadline 900 \
  --output /tmp/vocalis-latency-30-run1.json
```

Carga definida: 30 clientes HTTP independientes, cada uno con usuario nuevo, JWT propio y una evaluación. Tres lecturas de calentamiento por cliente se excluyen. Una barrera inicia los recorridos simultáneamente. Cada usuario realiza registro, login, 44 guardados secuenciales, recuperación al llegar a 20, envío, consulta del reporte y estado. Son hasta 50 solicitudes medidas por usuario (1.500 si todos finalizan). Carga cerrada: como máximo una petición en vuelo por usuario; no significa 30 peticiones simultáneas en cada instante ni una tasa de llegada constante.

El JSON incluye muestras crudas, estado HTTP/errores, recorridos completos, duración, throughput y p50/p95/p99 por operación (nearest-rank sobre respuestas HTTP correctas). Los errores y timeouts se contabilizan aparte y no deben ocultarse al citar percentiles. Se comprueba además el resultado OCEAN y el estado completado. No se mide renderizado ni tiempo hasta finalizar BPM; éste debe comprobarse aparte en outbox/Zeebe. El script devuelve error si algún recorrido falla.

Protocolo de medición:

1. Registrar commit **y estado del árbol de trabajo**, versiones instaladas, CPU/RAM, límites Docker, configuración de pools, modo Uvicorn, puerto y si cliente/servidor comparten máquina.
2. Confirmar salud de MySQL y Zeebe y banco BFI-44. Usar una base exclusiva; no reutilizar un alumno completado. No ejecutar pytest/build simultáneamente con la medición.
3. Para un criterio estadístico de entrega, repetir tres corridas de 30 usuarios en condiciones iguales, identificadas por separado. Aquí sólo se acreditó **una corrida final**; las corridas iniciales con fallos se conservaron como evidencia diagnóstica. El script genera usuarios nuevos por corrida.
4. Recoger `docker stats --no-stream`, logs de API/Zeebe, muestras y errores durante cada corrida. Informar resultados individuales, dispersión entre corridas y cantidad de muestras; 30 envíos por corrida dan poca precisión en p99.
5. El umbral local de 3 s se evaluó por petición HTTP con los percentiles que calcula el script; la única corrida final quedó por debajo. Repetir en un entorno representativo antes de afirmar un SLA o capacidad máxima.

## Pauta de usabilidad: cinco usuarios

Sin resultados todavía. Sesiones individuales, con datos ficticios: tres participantes en tareas de estudiante y dos en tareas de orientador, sin representar esa distribución como una muestra estadística de la población. Mantener el mismo guion y entorno. Explicar que se evalúa la interfaz, no la personalidad ni aptitud del participante; registrar consentimiento antes de grabar.

| Tarea | Criterio observable | Registrar |
|---|---|---|
| Registro y login | Identifica su rol, completa campos y entiende errores | Tiempo, errores, ayuda necesaria |
| Guardar y continuar (estudiante) | Sale con respuestas guardadas y las encuentra al volver | Respuestas recuperadas, confusión sobre guardado, éxito independiente |
| Finalizar y entender reporte (estudiante) | Completa BFI-44 y localiza puntajes; distingue exploración de recomendación validada | Abandonos, intentos de reedición, explicación del usuario en sus palabras |
| Panel y reporte (orientador) | Localiza alumno/curso y abre el reporte correcto | Tiempo, filtros, navegación y bloqueos |
| Estado e historial | Entiende fecha y estado real sin inferir actividad ficticia | Interpretaciones erróneas, necesidad de recargar, dudas |

Para cada tarea: éxito sin ayuda / con ayuda / no completada; tiempo inicio-fin; número de errores; observaciones y frase literal sólo si se recoge. Después: facilidad percibida de 1 a 7 y pregunta abierta «¿Qué cambiarías para entender mejor lo ocurrido?». No sumar tareas no aplicables al rol como fracasos. Al finalizar las cinco sesiones, reportar recuentos con denominador y roles, sin inventar promedios, satisfacción ni conclusiones previas. Priorizar impedimentos de completar/retomar/reportar; no ampliar el alcance del MVP a partir de sugerencias aisladas.

## Evidencias de esta ejecución

Artefactos locales temporales, con cuentas y variables privadas separadas de los resultados; no publicar `environment.json`, `accounts.json` ni credenciales.

- Suite y cobertura: `/tmp/vocalis-stage2-coverage.json`; **198 aprobadas**, incluidas **nueve MySQL**, cobertura combinada **89,80 %**.
- Demo MySQL/Zeebe sin recarga: `/tmp/vocalis-demo-58l1stz4/checks.json`; **26/26**. El broker de validación usó un directorio de datos en `/tmp` para sobrevivir al reinicio. El validador conservó temporalmente su BD UUID mediante `--keep-db` para navegador y carga; después se eliminó sólo esa BD y se retiró el broker temporal sin borrar volúmenes.
- Firefox 156.0.1: `/tmp/vocalis-browser-stage2-20260927/checks.json` y capturas PNG. Se visitaron `/auth`, `/estudiante/dashboard`, `/estudiante/evaluacion`, `/estudiante/reporte`, `/orientador/dashboard` y `/orientador/estudiante/:studentId/reporte` en **1440×900** y **390×844**. Se comprobaron registro/login/logout de ambos roles, estado vacío y 404 de estudiante, guardado parcial, salida/reingreso, 44 respuestas, reporte propio, bitácora, filtro y reporte autorizado del orientador, ausencia de desbordamiento horizontal y etiquetas del radar. Además se interceptó la red para verificar carga, error visible, botón Reintentar y recuperación del panel orientador. Las capturas usan datos sintéticos.
- Carga: `/tmp/vocalis-latency-stage2-30-after.json`. Máquina local AMD Ryzen 5 5600G (6 núcleos/12 hilos), 15 GiB RAM, Python 3.14.7, MySQL 8.0.46 en Docker, Zeebe 8.6.7 con límite de 2 GiB, Uvicorn normal y cliente en el mismo host. **30/30 recorridos, 1500 peticiones, cero errores, 9,398 s de duración, 159,6 peticiones/s.** p95 por operación: registro 1216,39 ms, login 706,77 ms, guardar 344,22 ms, reanudar 427,75 ms, enviar 423,45 ms, reporte 166,90 ms y estado 246,13 ms; máximo observado 1275,64 ms. Carga cerrada de 30 usuarios, sin tiempo de espera entre peticiones, timeout de 30 s, sin tests/build simultáneos. El script no mide duración de un recorrido completo, renderizado ni tiempo hasta `reporte_listo`.
- Corridas iniciales diagnósticas: `/tmp/vocalis-latency-stage2-30.json` y `/tmp/vocalis-latency-stage2-30-diagnostic.json`. Fallaron por conflictos MySQL de registro/primer guardado a alta concurrencia. El registro ahora libera el loop durante bcrypt y reintenta conflictos acotadamente; el guardado parcial reintenta deadlocks MySQL y devuelve 503 controlado si se agotan los intentos. Se añadieron pruebas de esos casos y una prueba opcional MySQL de registros concurrentes. Una corrida final exitosa no demuestra fiabilidad bajo cargas o duraciones distintas.

**Pendiente:** cinco sesiones de usabilidad con personas reales; revisión visual humana fuera del navegador headless, navegadores adicionales y despliegue completo de la imagen backend/Compose; tres corridas repetidas de carga en un entorno representativo; conciliación de ventanas extremas de recuperación BPM y asignación autorizada de cursos sin orientador cuando hay varios. Se conservan los permisos por `curso.orientador_id`. No se ejecutó seed destructivo sobre la BD de desarrollo, no se borraron volúmenes ajenos y no se creó release.
