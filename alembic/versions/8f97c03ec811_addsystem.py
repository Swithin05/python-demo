"""addsystem

Revision ID: 8f97c03ec811
Revises: cee1565497f2
Create Date: 2023-12-05 13:39:53.915269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8f97c03ec811"
down_revision: Union[str, None] = "cee1565497f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "systems",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("supreme_commander", sa.Text(), nullable=False),
        sa.Column("supreme_commander_name", sa.Text(), nullable=False),
        sa.Column("date_created", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("systems_pkey")),
        schema="interview",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("systems", schema="interview")
    # ### end Alembic commands ###
