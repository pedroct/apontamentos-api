"""unique index atividades nome (ci)

Revision ID: cb0a3479e4f0
Revises: 9b04caf050d3
Create Date: 2025-08-24 01:33:37.999236

"""

from alembic import op
import sqlalchemy as sa

revision = "cb0a3479e4f0"
down_revision = "9b04caf050d3"  # a última que você aplicou; ajuste se for diferente
branch_labels = None
depends_on = None


def upgrade() -> None:
    # índice único case-insensitive
    op.create_index(
        "uq_atividades_nome_lower",
        "atividades",
        [sa.text("lower(nome)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_atividades_nome_lower", table_name="atividades")
