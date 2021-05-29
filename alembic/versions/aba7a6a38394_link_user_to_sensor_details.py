"""link user to sensor details

Revision ID: aba7a6a38394
Revises: 7f1f9e2d2c3c
Create Date: 2021-05-29 03:18:41.415431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aba7a6a38394'
down_revision = '7f1f9e2d2c3c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        "fk_sensor_owner",
        "sensor_details", "users",
        ["owner"], ["id"],
        onupdate="CASCADE", ondelete="RESTRICT"
    )


def downgrade():
    op.drop_constraint("fk_sensor_owner", "sensor_details", type_="foreignkey")
