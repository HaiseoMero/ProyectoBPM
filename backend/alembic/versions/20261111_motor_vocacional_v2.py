"""Extensión no destructiva para Motor Vocacional v2 (divisiones Base 4 y 12 áreas SIES)."""
from alembic import op
import sqlalchemy as sa

revision = '20261111_motor_vocacional_v2'
down_revision = '20260924_bpm_outbox'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if inspector.has_table('reporte_vocacional'):
        existing_cols = {c['name'] for c in inspector.get_columns('reporte_vocacional')}
        for col_name in ('div_o', 'div_c', 'div_e', 'div_a', 'div_n', 'combinacion_id'):
            if col_name not in existing_cols:
                op.add_column('reporte_vocacional', sa.Column(col_name, sa.Integer(), nullable=True))

    if not inspector.has_table('area_estudio'):
        op.create_table(
            'area_estudio',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('slug', sa.String(64), nullable=False, unique=True),
            sa.Column('nombre', sa.String(120), nullable=False),
            sa.Column('area_sies', sa.String(80), nullable=False),
            sa.Column('descripcion', sa.String(600), nullable=False, server_default=''),
            sa.Column('ideal_o', sa.Float(), nullable=False),
            sa.Column('ideal_c', sa.Float(), nullable=False),
            sa.Column('ideal_e', sa.Float(), nullable=False),
            sa.Column('ideal_a', sa.Float(), nullable=False),
            sa.Column('ideal_n', sa.Float(), nullable=False),
            sa.Column('peso_o', sa.Float(), nullable=False, server_default='1.0'),
            sa.Column('peso_c', sa.Float(), nullable=False, server_default='1.0'),
            sa.Column('peso_e', sa.Float(), nullable=False, server_default='1.0'),
            sa.Column('peso_a', sa.Float(), nullable=False, server_default='1.0'),
            sa.Column('peso_n', sa.Float(), nullable=False, server_default='1.0'),
            sa.Column('carreras_json', sa.JSON(), nullable=False),
        )


def downgrade():
    raise RuntimeError('No eliminar automáticamente columnas ni catálogo de áreas vocacionales')
