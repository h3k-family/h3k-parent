"""create sensor table

Revision ID: 4795ecfe95fc
Revises: 
Create Date: 2021-05-29 00:16:28.400846

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

# revision identifiers, used by Alembic.
revision = '4795ecfe95fc'
down_revision = None
branch_labels = None
depends_on = None

# https://stackoverflow.com/a/33532154
# https://docs.sqlalchemy.org/en/14/core/compiler.html#further-examples


class utcnow(expression.FunctionElement):
    type = sa.DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


# TODO: https://github.com/sqlalchemy/sqlalchemy/issues/3444
# https://docs-sqlalchemy.readthedocs.io/ko/latest/core/defaults.html
# Look into updated_at not updating onupdate
def upgrade():
    op.create_table(
        "sensor_details",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("sensor_name", sa.String(100)),
        sa.Column("owner", sa.Integer),
        sa.Column("units_short", sa.String(20)),
        sa.Column("units_long", sa.String(50)),
        sa.Column("longitude", sa.Float),
        sa.Column("latitude", sa.Float),
        sa.Column("updated_at", sa.DateTime,
                  server_default=utcnow(), server_onupdate=utcnow()),
    )


def downgrade():
    op.drop_table("sensor_details")
