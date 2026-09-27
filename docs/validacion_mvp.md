# Validación integral del MVP de Vócalis

Fecha: 25 de septiembre de 2026. Fuente de verdad: código y ejecución local; `resumen_proyecto.md` se leyó como contexto y no se actualizó. No se creó ningún tag.

## Resultado y alcance

**La API y el recorrido BPM funcionan con el arranque de desarrollo `--reload` usado por Compose. El arranque sin `--reload` tiene un fallo confirmado del worker y no debe darse por aprobado.** La validación HTTP no sustituye la comprobación visual en navegador ni las sesiones de usabilidad.

| Verificación | Resultado | Evidencia/alcance |
|---|---|---|
| Suite backend completa | 186 aprobadas, 0 omitidas, 0 fallidas | Pytest, incluidas las siete pruebas MySQL opcionales |
| Cuatro pruebas MySQL de registro/migración/seed | 4 aprobadas | `tests/test_registro_mysql.py`; cada fixture crea y elimina su propia BD UUID |
| Tres pruebas MySQL de consistencia BPM | 3 aprobadas | `tests/test_bpm_mysql.py`; transacciones y bloqueos reales, RPC Zeebe simulados en estos tests |
| Frontend existente | 4 aprobadas | `node --test tests/frontend/reporte-neutral.test.mjs`; renderizado de plantilla, no navegador |
| Compilación frontend | Aprobada | `npm run build` |
| ESLint de las cuatro vistas principales y util BPM | Aprobado | Sin `--fix`; no se editaron componentes |
| Revisión del diff | Aprobada | `git diff --check` y comprobación de espacios de los tres archivos nuevos no indexados |
| Registro estudiante/orientador y asociación | Aprobados vía HTTP real | Código privado aleatorio; alumno sólo en el curso del orientador del establecimiento correspondiente |
| Guardar, cerrar sesión lógica y continuar | Aprobado vía HTTP real | Guardadas 20 respuestas, nuevo login, recuperadas desde MySQL y completadas las 44 |
| Envío y OCEAN | Aprobados vía HTTP real | 44 valores 3 producen cinco puntajes 0,5; envío final persiste las 44 respuestas |
| Reportes y permisos | Aprobados vía HTTP real | Contratos iguales entre consulta propia, por ID y por orientador; alumno ajeno 404 y orientador ajeno 403 |
| Una evaluación y bloqueo posterior | Aprobados | Reanudación conserva una fila; edición y reenvío completados devuelven 400 |
| Migraciones MySQL 8.0.46 | Aprobadas en BD nueva | Inicialización del esquema y `alembic upgrade head` hasta `20260924_bpm_outbox`; migraciones sobre datos antiguos cubiertas además por los tests MySQL |
| Despliegue e inicio Zeebe 8.6.7 | Aprobados | BPMN original desplegado, clave real persistida; mensajes correlacionados y jobs creados |
| Avance BPM con `--reload` | Aprobado en recorrido normal | API estudiante observó `calculando_ocean` y `reporte_listo`; endpoint orientador también refleja el estado final |
| Caída del broker | Reporte conservado y publicación recuperada | Se detuvo sólo el broker temporal; el evento quedó pendiente y el reporte siguió disponible |
| Recuperación BPM completa con `--reload` | Aprobada | Tras reiniciar Zeebe llega a `reporte_listo`; evento `consumido`, sin reenviar el cuestionario |
| Arranque sin `--reload` | **Fallido** | No llega a `reporte_listo`; detalles abajo |
| Estados visibles en navegador | Pendiente manual | Se comprobaron contratos y mapeo en código; no se ejecutó una sesión de navegador automatizada |
| Latencia con 30 usuarios | Procedimiento preparado, no medida | No hay resultados de rendimiento ni aprobación de un SLA |
| Usabilidad con cinco participantes | Pauta preparada, no ejecutada | No se atribuyen opiniones ni resultados a usuarios inexistentes |

### Fallo reproducido durante la validación

Con `uvicorn app.main:app` sin recarga, el canal gRPC creado al importar `app/worker.py:10-11` queda asociado a un bucle distinto del usado por `worker.work()` (`app/worker.py:55`). Se observó `RuntimeError: ... Future ... attached to a different loop` en los tres pollers. Uvicorn 0.52.4 hace una carga anticipada de la aplicación en este modo. La tarea creada en `app/main.py:19` falla, pero la API sigue respondiendo; su excepción se recoge con `return_exceptions=True` al cerrar (`app/main.py:26`) y no acredita salud BPM.

Se reprodujo en Python 3.14.7 local y en Python 3.11.16 de la imagen backend disponible. La imagen contiene las mismas versiones de pyzeebe/gRPC/Uvicorn, aunque está desactualizada respecto a `aiosqlite`; esta comprobación Docker fue diagnóstica, no una certificación de una imagen reconstruida con todos los requirements actuales.

En la ejecución normal fallaron tres comprobaciones: llegada a `reporte_listo`, estado final del endpoint orientador y finalización tras recuperar el broker. El mensaje sí se publicó, se correlacionó y creó `calcular-ocean`. Con `--reload`, usado por el Compose actual, el worker Docker consumió los jobs pendientes de ambas evaluaciones hasta `reporte_listo`; después se repitió la demo desde una BD y un broker nuevos: **25 comprobaciones aprobadas**, incluida la recuperación completa tras la caída.

Corrección pendiente recomendada: crear/cerrar el canal y el worker dentro del ciclo asíncrono del lifespan, supervisar su tarea y añadir una prueba del arranque real sin recarga. **No se modificó código del producto para ocultar este resultado.** `--reload` permite la demo de desarrollo, pero no constituye una solución para despliegue sin recarga.

### Recuperación y límites

Se verificó una caída real después de iniciar la instancia y antes de publicar el cuestionario. El reporte quedó confirmado, la consulta devolvió 200 y `bpm_evento` quedó `pendiente` con `ZeebeGatewayUnavailableError`. Tras reiniciar el mismo broker, el proceso de reintento publicó el evento sin repetir el envío HTTP del estudiante. Las trazas del broker permiten distinguir publicación, correlación y ejecución de jobs. En la demo final se comprobaron dos publicaciones y seis jobs completados (los tres tipos por cada instancia), deduplicando los registros del exporter por partición y posición para no contar de nuevo los reproducidos durante el reinicio.

Las pruebas automatizadas adicionales cubren fallo de commit, fallo de publicación, reintentos, solicitudes repetidas y competencia de sesiones MySQL. No equivalen a una prueba de todas las ventanas de caída posibles. Siguen fuera de la evidencia de esta ejecución: caída justo después de aceptación remota antes del commit local, apagones prolongados, expiración de 23/24 horas, conciliación de inicios `incierto`, pérdida de disco y múltiples réplicas backend. Véase `backend/BPM_RECOVERY.md`. No se afirma una garantía distribuida de exactly-once.

Los paneles consumen el estado al cargar la vista (`StudentDashboardView.vue:219`, `OrientadorDashboardView.vue:233`); no hay sondeo continuo. Para la demo se debe recargar/volver a entrar. Los estados intermedios pueden transcurrir entre dos lecturas. `src/utils/bpmStatus.js` traduce `registro`, `calculando_ocean`, `generando_reporte`, `reporte_listo`; null/desconocido se muestra neutral. No se insertaron estados artificiales en MySQL para simular el avance.

## Cobertura backend medida

Medición con coverage.py 7.16.1, `source=['app']`, ramas activadas, sin excluir `main.py`, workers ni archivos con cobertura baja. Denominador: código Python de `backend/app`, no tests ni migraciones.

| Métrica | Resultado |
|---|---|
| Líneas ejecutadas | **812 / 957 = 84,85 %** |
| Ramas ejecutadas | **159 / 196 = 81,12 %** |
| Combinación líneas + ramas de coverage.py | **84,22 %** |

Los 186 tests son un conteo, no un porcentaje de cobertura. Esta medición corresponde a pytest; la demo externa se registra por separado y no se sumó artificialmente a la cobertura. `app/main.py` y `app/worker.py` tienen 0 % en esa suite. Esto explica por qué el fallo de arranque pudo coexistir con todos los tests aprobados.

Desglose: autenticación/registro 37; respuestas BFI-44 30; reportes 53; reglas vocacionales 29; entrega BPM 15; estado orientador 6; OCEAN 4; migración evaluación 3; migración registro 2; MySQL registro 4 y MySQL BPM 3.

Reproducción desde `backend/`, con un entorno virtual activo y la URL administrativa del laboratorio configurada:

```bash
python -m pip install coverage==7.16.1
export PYTHONDONTWRITEBYTECODE=1
export COVERAGE_FILE=/tmp/vocalis-mvp.coverage
python -B -m coverage run --branch --source=app -m pytest tests -q -ra -p no:cacheprovider
python -B -m coverage report
python -B -m coverage json -o /tmp/vocalis-coverage.json
python -B -m coverage html -d /tmp/vocalis-coverage-html
```

Sin `VOCALIS_TEST_MYSQL_ADMIN_URL` se omiten **siete**, no cuatro, pruebas. No se deben presentar como aprobadas. Con esa variable, los fixtures crean bases `vocalis_test_registro_<uuid>` y sólo eliminan esas mismas bases. El test que invoca el seed destructivo lo hace únicamente dentro de su BD temporal.

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
  --gateway 127.0.0.1:27650 --zeebe-container vocalis-validation-zeebe --reload
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

Para reproducir el fallo de arranque quitar `--reload`; `--diagnose-worker` añade un observador temporal que registra la excepción y vuelve a lanzarla, sin reemplazar los workers ni sus transacciones. La demo aprobada no necesita ese observador.

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
subprocess.run([sys.executable, '-B', '-m', 'uvicorn', 'app.main:app', '--reload',
                '--reload-dir', 'app', '--host', '127.0.0.1', '--port', '8000'], env=env, check=True)
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
- Comprobar «Mi Historial», fechas reales, errores de conexión y reintentos; distinguir controles fuera del MVP, como PDF, de funciones implementadas.
- Registrar navegador/versión, capturas con datos sintéticos, pasos, resultado esperado/obtenido y cualquier incidencia. No dar estos pasos por aprobados sin ejecutarlos visualmente.

### 5. Cierre seguro del laboratorio

Archivar sólo evidencia sin secretos. Verificar propietario y etiqueta antes de limpiar. El validador elimina su BD salvo `--keep-db`; si se conserva, tomar el nombre exacto de `runtime.json` y eliminar **sólo esa BD** después de terminar la demo. No usar comodines, `docker volume prune` ni `docker compose down -v` sobre el proyecto existente.

```bash
# Sólo los recursos que se crearon con los comandos de esta guía.
docker inspect vocalis-validation-zeebe --format '{{ index .Config.Labels "vocalis.validation" }}'
docker rm -f -v vocalis-validation-zeebe
# Si se creó el MySQL aislado de esta guía, y una vez terminadas todas las pruebas:
docker rm -f "$DEMO_MYSQL"
docker volume rm "$DEMO_MYSQL_VOLUME"
unset MYSQL_ROOT_PASSWORD VOCALIS_TEST_MYSQL_ADMIN_URL
```

## Procedimiento de latencia: 30 usuarios concurrentes

Se preparó `backend/scripts/measure_latency.py`; no se ejecutó la medición de 30 usuarios. Su destino debe ser la API del laboratorio conservado, nunca la BD de desarrollo con datos ajenos.

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
3. Hacer una corrida de ensayo no reportada, luego tres corridas de 30 usuarios en condiciones iguales, identificadas por separado. El script genera usuarios nuevos por corrida. Documentar si se reinicia la BD/broker entre corridas; no mezclar una ejecución fría con otras calientes sin indicarlo.
4. Recoger `docker stats --no-stream`, logs de API/Zeebe, muestras y errores durante cada corrida. Informar resultados individuales, dispersión entre corridas y cantidad de muestras; 30 envíos por corrida dan poca precisión en p99.
5. Definir el umbral de aceptación antes de medir. No hay un SLA verificado en esta entrega. No extrapolar estas mediciones locales a Internet ni a capacidad máxima.

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

Artefactos locales temporales; guardar una copia sin secretos si se necesita permanencia:

- Suite/cobertura: `/tmp/vocalis-mvp-coverage-5jby5rd8/` (`tests.xml`, `coverage.json`, HTML).
- Demo sin recarga: `/tmp/vocalis-demo-1_8_s8nt/` (checks, outbox, trazas del broker).
- Demo completa con recarga: `/tmp/vocalis-demo-_237_7zx/` (25 checks aprobados, ambos eventos de completar consumidos).
- Diagnóstico local/Docker: `/tmp/vocalis-demo-fm23tlur/` (excepción de worker, modo Docker con/sin recarga).

Al terminar se eliminaron las tres bases de demo creadas (una conservada sólo durante el diagnóstico) y los contenedores de validación; no quedaron esos servicios ejecutándose. Las siete bases temporales de pytest se eliminaron mediante sus fixtures. No se ejecutó el seed sobre la BD existente.

Los archivos nuevos del repositorio son este informe, `backend/scripts/validate_mvp.py` y `backend/scripts/measure_latency.py`. Se conservaron los cambios preexistentes; no se modificaron algoritmos, modelos, migraciones, Docker, BPMN, frontend, `resumen_proyecto.md` ni `WordBPM.docx`. La creación del tag `v1.0-mvp` sigue pendiente de demo manual completa y autorización explícita del propietario.
