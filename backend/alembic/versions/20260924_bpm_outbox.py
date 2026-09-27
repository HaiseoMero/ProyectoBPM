"""Bandeja de entrega Zeebe; no reenvía eventos históricos de resultado desconocido."""
from alembic import op
import sqlalchemy as sa

revision = '20260924_bpm_outbox'
down_revision = '20260922_registro_contexto'
branch_labels = None
depends_on = None


def upgrade():
    if sa.inspect(op.get_bind()).has_table('bpm_evento'):
        return  # Compatible con create_all del modelo actualizado.
    op.create_table(
        'bpm_evento',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('evaluacion_id', sa.Integer(), sa.ForeignKey('evaluacion.id'), nullable=False),
        sa.Column('tipo', sa.String(20), nullable=False),
        sa.Column('message_id', sa.String(36), nullable=False, unique=True),
        sa.Column('estado', sa.String(20), nullable=False),
        sa.Column('intentos', sa.Integer(), nullable=False),
        sa.Column('primer_intento', sa.DateTime(), nullable=True),
        sa.Column('proximo_intento', sa.DateTime(), nullable=True),
        sa.Column('ultimo_error', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('evaluacion_id', 'tipo', name='uq_bpm_evento_evaluacion_tipo'),
    )


def downgrade():
    raise RuntimeError('No borrar automáticamente eventos de entrega pendientes o su trazabilidad')
