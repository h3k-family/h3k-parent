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


sensor_details_table = sa.Table(
    "sensor_details",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("sensor_name", sa.String(100)),
    sa.Column("owner", sa.Integer),  # Add foreign key relationship
    sa.Column("units_short", sa.String(20)),
    sa.Column("units_long", sa.String(50)),
    sa.Column("longitude", sa.Float),
    sa.Column("latitude", sa.Float),
    sa.Column("updated_at", sa.DateTime, server_default=utcnow()),
)


class SensorDetails(BaseModel):
    sensor_name: str
    units_short: str
    units_long: str
    longitude: float
    latitude: float


sensor_data_table = sa.Table(
    "sensor_data",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("sensor_id", sa.Integer),
    sa.Column("value", sa.Float),
    sa.Column("updated_at", sa.DateTime,
              server_default=utcnow(), server_onupdate=utcnow()),
)


class SensorData(BaseModel):
    sensor_id: int
    value: float
