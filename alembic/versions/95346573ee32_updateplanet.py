"""updateplanet

Revision ID: 95346573ee32
Revises: 8eefef142f0a
Create Date: 2023-12-05 13:58:39.888876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "95346573ee32"
down_revision: Union[str, None] = "8eefef142f0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "planets", sa.Column("system_id", sa.UUID(), nullable=False), schema="interview"
    )
    op.create_foreign_key(
        op.f("planets_system_id_fkey"),
        "planets",
        "systems",
        ["system_id"],
        ["id"],
        source_schema="interview",
        referent_schema="interview",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("planets_system_id_fkey"),
        "planets",
        schema="interview",
        type_="foreignkey",
    )
    op.drop_column("planets", "system_id", schema="interview")
    # ### end Alembic commands ###
