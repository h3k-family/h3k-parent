"""create children table

Revision ID: a1fcf449a092
Revises: 7f1f9e2d2c3c
Create Date: 2021-05-29 06:35:39.679090

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

# revision identifiers, used by Alembic.
revision = 'a1fcf449a092'
down_revision = '7f1f9e2d2c3c'
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
        "children",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("url", sa.String(100), unique=True),
        sa.Column("updated_at", sa.DateTime,
                  server_default=utcnow(), server_onupdate=utcnow()),
    )


def downgrade():
    op.drop_table("children")
