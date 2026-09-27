"""Contexto institucional y fecha de nacimiento, sin inventar datos históricos."""
from alembic import op
import sqlalchemy as sa

revision = "20260922_registro_contexto"
down_revision = "20260922_eval_unique"
branch_labels = None
depends_on = None

CONSTRAINT_NAME = "uq_curso_establecimiento_nombre"


def upgrade() -> None:
    if op.get_context().as_sql:
        raise RuntimeError("Se requiere conexión para comprobar los cursos existentes")
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    for table in ("curso", "estudiante", "orientador"):
        if not inspector.has_table(table):
            raise RuntimeError(f"Falta la tabla inicial {table}")
    duplicates = connection.execute(sa.text(
        "SELECT 1 FROM curso GROUP BY establecimiento, nombre HAVING COUNT(*) > 1 LIMIT 1"
    )).first()
    if duplicates:
        raise RuntimeError("Hay cursos duplicados por establecimiento y nombre; resolverlos explícitamente")

    # Primero UNIQUE: si aparece un duplicado concurrente, fallar sin añadir columnas.
    unique = inspector.get_unique_constraints("curso") + inspector.get_indexes("curso")
    if not any(
        set(item["column_names"]) == {"establecimiento", "nombre"}
        and item.get("unique", True) for item in unique
    ):
        with op.batch_alter_table("curso") as batch:
            batch.create_unique_constraint(CONSTRAINT_NAME, ["establecimiento", "nombre"])
    if "establecimiento" not in {c["name"] for c in inspector.get_columns("orientador")}:
        op.add_column("orientador", sa.Column("establecimiento", sa.String(255), nullable=True))
    if "fecha_nacimiento" not in {c["name"] for c in inspector.get_columns("estudiante")}:
        op.add_column("estudiante", sa.Column("fecha_nacimiento", sa.Date(), nullable=True))


def downgrade() -> None:
    # Evitar pérdida inadvertida de fechas y contexto institucional ya registrados.
    raise RuntimeError("Downgrade destructivo no automático: requiere preservar los nuevos datos")
