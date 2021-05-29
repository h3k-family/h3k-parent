import sqlalchemy as sa
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from pydantic import BaseModel
from api.models import meta

# https://stackoverflow.com/a/33532154
# https://docs.sqlalchemy.org/en/14/core/compiler.html#further-examples


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


children_table = sa.Table(
    "children",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("url", sa.Text, unique=True),
    sa.Column("updated_at", sa.DateTime,
              server_default=utcnow(), server_onupdate=utcnow()),
)


class Child(BaseModel):
    url: str
