from fastapi import APIRouter, Depends
from sqlalchemy import exc
from api.models import con
from auth.auth import get_current_active_user
from auth.models import DbUser
from .models import sensor_details_table, SensorDetails


router = APIRouter(tags=["sensors"])


@router.post("/add_sensor/")
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
