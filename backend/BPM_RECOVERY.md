# Entrega transaccional MySQL → Zeebe

## Flujo implementado

- La primera respuesta, evaluación, `ProcesoBPM` y evento `iniciar` se confirman juntos. `start_process()` no publica ni hace commit. Después del commit se intenta crear la instancia; se extrae la key de la respuesta de pyzeebe.
- El envío final confirma respuestas definitivas, reporte, `completed_at` y evento `completar` en **una transacción MySQL**. Solo después intenta publicar `CuestionarioCompletado`. Un commit fallido no publica.
- `bpm_evento` tiene UNIQUE por `(evaluacion_id, tipo)` y un `message_id` UUID estable. No cambia el contrato HTTP ni `bpm_estado`: los estados de entrega son técnicos y separados de los cuatro estados BPM existentes.
- El lifespan de la API ejecuta un reintento cada 5 segundos, con espera entre fallos hasta 300 segundos. Usa sesiones nuevas y recupera eventos persistidos tras reiniciar. Cada RPC tiene un límite de 5 segundos. Si el backend está detenido no hay reintentos hasta su próximo arranque.
- `FOR UPDATE SKIP LOCKED` excluye despachadores simultáneos durante el RPC. La API conserva el reporte aunque falle Zeebe o la confirmación local de la entrega. Una petición final repetida mantiene el rechazo 400 existente, sin editar ni producir otro reporte/evento.
- Los workers exigen reporte y evaluación completados, validan `job.process_instance_key`, aceptan duplicados sin retroceder y rechazan saltos. El primer worker confirma el evento como `consumido` en la misma transacción del avance BPM.
- Los errores de integración se registran como JSON mediante logging: evento, identificadores, estado y clase de error, sin payloads de respuestas.

## Caídas, ambigüedad e idempotencia

1. **Zeebe caído antes del RPC:** falla la comprobación de topología; el reporte sigue disponible y el evento queda `pendiente`, con error y próximo intento. No se inicia la ventana de deduplicación. Se recupera automáticamente al volver Zeebe, incluso tras reiniciar la API.
2. **Publicación con respuesta perdida:** el primer intento se registra antes del RPC. Se reutiliza el mismo `message_id`, nombre y correlación; `MessageAlreadyExistsError` equivale a confirmación. TTL de 24 horas y reintento automático hasta 23 horas desde el primer intento. Después se requiere `revision`, sin volver a publicar automáticamente.
3. **Aceptación confirmada:** `enviado` evita nuevas publicaciones. No significa que el proceso terminó. Si ningún worker acredita consumo antes del TTL, pasa a `revision`; un worker tardío válido todavía puede confirmar `consumido`.
4. **Inicio de instancia incierto:** antes de `run_process` se persiste `incierto`. Si se pierde su respuesta o falla el commit de la key, no se crea otra instancia automáticamente. La topología inaccesible antes de intentar crear, o un rechazo explícito por definición inexistente, sí permiten reintentar. El evento final espera una key confirmada, sin afirmar avance BPM.

No existe una transacción distribuida ni garantía general de «exactamente una publicación»: puede repetirse un intento de red tras perderse un acuse. La deduplicación de Zeebe solo se aplica mientras retiene el mensaje. La instancia única y el receiveTask sin bucles del BPMN actual, más los workers idempotentes, evitan repetir los efectos del flujo normal. Instancias duplicadas creadas externamente, pérdida de datos del broker, cambios del BPMN, pausas extremas del proceso o alteraciones de relojes requieren conciliación. No se promete recuperación automática ilimitada de resultados ambiguos.

Referencia: [mensajes y unicidad en Camunda 8.6](https://unsupported.docs.camunda.io/8.6/docs/components/concepts/messages/).

## Migración y datos históricos

`20260924_bpm_outbox` sucede a `20260922_registro_contexto`; solo crea `bpm_evento`. No modifica reportes/evaluaciones existentes ni genera eventos históricos: antes de este cambio no hay evidencia durable para saber cuáles fueron publicados. `create_all` no reemplaza Alembic. Ejecutar desde `backend`, con copia de seguridad y el backend detenido durante el despliegue:

```bash
venv/bin/python -B -m alembic upgrade head
```

El downgrade no elimina automáticamente la trazabilidad. La migración se prueba en MySQL temporal, comprobando conservación de datos y unicidad. Los reportes históricos sin proceso o key válida requieren revisión explícita; nunca se recrean instancias a ciegas.

## Conciliación operativa

Consulta de solo lectura para diagnosticar pendientes:

```sql
SELECT id, evaluacion_id, tipo, estado, message_id, intentos,
       primer_intento, proximo_intento, ultimo_error
FROM bpm_evento
WHERE estado IN ('pendiente', 'incierto', 'revision')
ORDER BY id;
```

Para un inicio `incierto`, detener la API/despachadores y comprobar en Operate la instancia de `evaluacion-vocacional` y su variable `evaluacion_id`. Si existe exactamente una, reconciliar en una transacción su key en `proceso_bpm` y el evento `iniciar` como `enviado`; el mensaje final pendiente se reanudará al arrancar. Si se demuestra que no existe ninguna instancia ni solicitud en vuelo, puede restablecerse ese evento a `pendiente`, limpiando próximo/primer intento y error. No hacer ese cambio basándose solamente en un timeout o en un índice de Operate todavía incompleto.

Para mensajes en `revision` o reportes históricos, comprobar primero instancia, receiveTask, mensaje y trabajos pendientes. No reiniciar la ventana ni cambiar el UUID indiscriminadamente. Si no puede verificarse el resultado, mantener la revisión pendiente. No se añade un endpoint público que permita saltarse esta conciliación.

## Evidencia y límites de pruebas

Las pruebas permanentes cubren rollback sin publicación, reporte visible antes del RPC, gateway gRPC realmente inaccesible, error/acuse perdido, identidad estable al reintentar, rechazo de envíos repetidos, recuperación periódica, inicio incierto y transiciones de workers. `test_bpm_mysql.py` comprueba con conexiones MySQL reales dos envíos simultáneos, despachadores concurrentes y migración; requiere `VOCALIS_TEST_MYSQL_ADMIN_URL` y crea/elimina únicamente sus bases temporales. Zeebe se simula en esas pruebas de aceptación: **no acreditan el recorrido E2E con Camunda real** ni rendimiento bajo carga.

## Verificación realizada — 24/09/2026

- Suite completa: **98 aprobadas**, sin omisiones, con `VOCALIS_TEST_MYSQL_ADMIN_URL` configurada. Incluye siete pruebas MySQL (cuatro de registro existentes y tres nuevas de entrega/migración).
- Migración aplicada en MySQL 8.0.46 de desarrollo: `alembic_version = 20260924_bpm_outbox`. Se compararon todas las filas anteriores y se conservaron sin cambios; `bpm_evento` quedó vacía, sin publicaciones históricas.
- Respaldo previo: `/tmp/vocalis-before-bpm-outbox-ii1fy1j5.sql`.
- La indisponibilidad gRPC se probó con una conexión local real rechazada; no se ejecutó una evaluación E2E contra un Zeebe operativo. Los casos de aceptación/deduplicación del broker usan dobles de prueba.
