"""create user table

Revision ID: 7f1f9e2d2c3c
Revises: 4795ecfe95fc
Create Date: 2021-05-29 02:56:05.034685

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles

# revision identifiers, used by Alembic.
revision = '7f1f9e2d2c3c'
down_revision = '4795ecfe95fc'
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
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(100)),
        sa.Column("email", sa.String(100)),
        sa.Column("password", sa.String(100)),
        sa.Column("disabled", sa.Boolean),
        sa.Column("updated_at", sa.DateTime,
                  server_default=utcnow(), server_onupdate=utcnow()),
    )


def downgrade():
    op.drop_table("users")
