from fastapi import APIRouter, Depends
from sqlalchemy import exc
import sqlalchemy as sa
from api.models import con
from auth.auth import get_current_active_user
from auth.models import DbUser, user_table
from .models import sensor_details_table, SensorDetails
from .models import sensor_data_table, SensorData


router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.post("/add/")
async def add_sensor_details(sensor: SensorDetails,
                             current_user: DbUser = Depends(get_current_active_user)):
    query = sensor_details_table.insert().values(
        sensor_name=sensor.sensor_name,
        owner=current_user.id,
        units_short=sensor.units_short,
        units_long=sensor.units_long,
        longitude=sensor.longitude,
        latitude=sensor.latitude
    )
    try:
        result = con.execute(query)
    except exc.SQLAlchemyError:
        return {"error": "could not save record"}

    return {"inserted_at": result.inserted_primary_key}


@router.post("/data/add/")
async def add_sensor_data(sensor_data: SensorData,
                          _current_user: DbUser = Depends(get_current_active_user)):
    query = sensor_data_table.insert().values(
        sensor_id=sensor_data.sensor_id,
        value=sensor_data.value,
    )
    try:
        result = con.execute(query)
    except exc.SQLAlchemyError:
        return {"error": "could not save record"}

    return {"inserted_at": result.inserted_primary_key}


@router.get("/data/")
async def get_all_sensor_data():
    sttmt = sa.select(
        sensor_data_table,
        sensor_details_table.c.sensor_name,
        user_table.c.username,
        sensor_details_table.c.units_short,
        sensor_details_table.c.units_long,
        sensor_details_table.c.latitude,
        sensor_details_table.c.longitude,
    ).join(
        sensor_details_table,
        sensor_data_table.c.sensor_id == sensor_details_table.c.id
    ).join(
        user_table, sensor_details_table.c.owner == user_table.c.id
    )
    results = con.execute(sttmt)
    to_return = []
    for result in results:
        to_return.append(result)
    return to_return
