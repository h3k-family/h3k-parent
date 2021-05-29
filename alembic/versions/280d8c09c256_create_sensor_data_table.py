"""create sensor data table

Revision ID: 280d8c09c256
Revises: aba7a6a38394
Create Date: 2021-05-29 03:27:59.736370

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

# revision identifiers, used by Alembic.
revision = '280d8c09c256'
down_revision = 'aba7a6a38394'
branch_labels = None
depends_on = None

# https://stackoverflow.com/a/33532154
# https://docs.sqlalchemy.org/en/14/core/compiler.html#further-examples


class utcnow(expression.FunctionElement):
    type = sa.DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def upgrade():
    op.create_table(
        "sensor_data",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("sensor_id", sa.Integer),
        sa.Column("value", sa.Float),
        sa.Column("updated_at", sa.DateTime,
                  server_default=utcnow(), server_onupdate=utcnow()),
    )
    op.create_foreign_key(
        "fk_sensor_details_data",
        "sensor_data", "sensor_details",
        ["sensor_id"], ["id"],
        onupdate="CASCADE", ondelete="RESTRICT"
    )


def downgrade():
    op.drop_constraint("fk_sensor_details_data",
                       "sensor_data", type_="foreignkey")
    op.drop_table("sensor_data")
