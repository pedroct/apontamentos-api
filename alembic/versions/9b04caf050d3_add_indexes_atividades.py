"""add indexes atividades

Revision ID: 9b04caf050d3
Revises: e43a9efa1956
Create Date: 2025-08-24 01:15:04.560674

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "9b04caf050d3"
down_revision = "e43a9efa1956"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_atividades_ativo", "atividades", ["ativo"])
    op.create_index("ix_atividades_criado_em", "atividades", ["criado_em"])
    op.create_index("ix_atividades_nome", "atividades", ["nome"])


def downgrade() -> None:
    op.drop_index("ix_atividades_nome", table_name="atividades")
    op.drop_index("ix_atividades_criado_em", table_name="atividades")
    op.drop_index("ix_atividades_ativo", table_name="atividades")
