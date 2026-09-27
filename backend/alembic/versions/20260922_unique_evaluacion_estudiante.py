"""Una evaluación por estudiante sobre el esquema existente de create_all.

Revision ID: 20260922_eval_unique
Revises: None
"""
from alembic import op
import sqlalchemy as sa

revision = "20260922_eval_unique"
down_revision = None
branch_labels = None
depends_on = None

CONSTRAINT_NAME = "uq_evaluacion_estudiante"


def upgrade() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("Esta migración requiere conexión para comprobar duplicados.")

    connection = op.get_bind()
    inspector = sa.inspect(connection)
    if not inspector.has_table("evaluacion"):
        raise RuntimeError(
            "Falta el esquema inicial: esta revisión modifica las tablas existentes "
            "creadas por Base.metadata.create_all; no crea el esquema completo."
        )

    duplicates = connection.execute(sa.text(
        "SELECT estudiante_id, COUNT(*) AS cantidad FROM evaluacion "
        "GROUP BY estudiante_id HAVING COUNT(*) > 1 LIMIT 10"
    )).all()
    if duplicates:
        raise RuntimeError(
            "No se aplicó UNIQUE: hay estudiantes con varias evaluaciones "
            f"(hasta 10 casos): {duplicates}. Resolverlos explícitamente sin "
            "eliminar respuestas o reportes automáticamente y volver a ejecutar."
        )

    # create_all con el modelo actualizado puede haber creado ya la restricción.
    constraints = inspector.get_unique_constraints("evaluacion")
    indexes = inspector.get_indexes("evaluacion")
    if any(c["column_names"] == ["estudiante_id"] for c in constraints) or any(
        i.get("unique") and i["column_names"] == ["estudiante_id"] for i in indexes
    ):
        return

    with op.batch_alter_table("evaluacion") as batch_op:
        batch_op.create_unique_constraint(CONSTRAINT_NAME, ["estudiante_id"])


def downgrade() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("Esta migración requiere conexión para comprobar restricciones.")
    constraints = sa.inspect(op.get_bind()).get_unique_constraints("evaluacion")
    if not any(c["name"] == CONSTRAINT_NAME for c in constraints):
        return
    with op.batch_alter_table("evaluacion") as batch_op:
        batch_op.drop_constraint(CONSTRAINT_NAME, type_="unique")
