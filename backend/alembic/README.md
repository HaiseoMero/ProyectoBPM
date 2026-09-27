# Unicidad de evaluación por estudiante

La revisión `20260922_eval_unique` añade `uq_evaluacion_estudiante` al esquema
existente, originalmente creado mediante `Base.metadata.create_all`.
No es una migración de creación del esquema completo.

Antes de aplicarla, con la API y los workers detenidos y una copia de seguridad,
revisar la BD de destino:

```sql
SELECT estudiante_id, COUNT(*) AS cantidad
FROM evaluacion
GROUP BY estudiante_id
HAVING COUNT(*) > 1;
```

Si hay duplicados, decidir explícitamente cómo conservar evaluaciones, respuestas,
reportes y procesos asociados. La migración comprueba de nuevo los duplicados y
aborta sin eliminarlos ni fusionarlos. No ejecutar el seed para resolverlos:
el seed borra las tablas.

Desde `backend`, con `DATABASE_URL` apuntando al destino revisado:

```sh
venv/bin/python -m alembic upgrade head
```

La comprobación requiere conexión; no admite `--sql`. `create_all` no actualiza
tablas existentes, por lo que cambiar el modelo no sustituye esta migración.
En una instalación nueva, crear primero el esquema por el mecanismo existente;
si la unicidad ya existe, el upgrade no la duplica.
