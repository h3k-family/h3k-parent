import os
from fastapi import FastAPI
import sqlalchemy as sa
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from dotenv import load_dotenv
from pydantic import BaseModel
from auth import auth

load_dotenv()


app = FastAPI(
    title="h3k-child API",
    description="Haba na haba, hujaza kibaba. Part of the h3k project.",
    version="0.0.1",
)

app.include_router(auth.router)


# https://stackoverflow.com/a/33532154
# https://docs.sqlalchemy.org/en/14/core/compiler.html#further-examples
class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def connect():
    user = os.environ.get("DB_USER")
    db_name = os.environ.get("DB_NAME")
    db_pass = os.environ.get("DB_PASS")
    db_port = os.environ.get("DB_PORT")
    db_host = os.environ.get("DB_HOST")
    #  print(user, db_name, db_pass)
    #  print(user, db_pass, db_host, db_port, db_name)
    url = "postgresql://{}:{}@{}:{}/{}"
    url = url.format(user, db_pass, db_host, db_port, db_name)
    # The return value of create_engine() is our connection object
    connection = sa.create_engine(url, client_encoding="utf8")
    # We then bind the connection to MetaData()
    metadata = sa.MetaData(bind=connection)

    return connection, metadata


con, meta = connect()

sensor_details_table = sa.Table(
    "sensor_details",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("sensor_name", sa.String(100)),
    sa.Column("units_short", sa.String(20)),
    sa.Column("units_long", sa.String(50)),
    sa.Column("updated_at", sa.DateTime, server_default=utcnow()),
)


class SensorDetails(BaseModel):
    sensor_name: str
    units_short: str
    units_long: str


@app.post("/add_sensor/")
async def add_sensor_details(sensor: SensorDetails):
    query = sensor_details_table.insert().values(
        sensor_name=sensor.sensor_name,
        units_short=sensor.units_short,
        units_long=sensor.units_long
    )
    result = con.execute(query)
    return {"inserted_at": result.inserted_primary_key}


@app.get("/")
async def root():
    return {"message": "Hello World"}
