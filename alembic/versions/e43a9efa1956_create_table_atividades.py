"""create table atividades

Revision ID: e43a9efa1956
Revises: d2fbb0ae9bbd
Create Date: 2025-08-23 23:00:38.311311

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "e43a9efa1956"  # mantenha o valor real do arquivo
down_revision = "d2fbb0ae9bbd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "atividades",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("descricao", sa.Text, nullable=True),
        sa.Column("ativo", sa.Boolean, nullable=False, server_default=sa.text("true")),
        sa.Column(
            "criado_em",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("atividades")
