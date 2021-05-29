from fastapi import APIRouter
from api.models import con
from .models import sensor_details_table, SensorDetails


router = APIRouter(tags=["sensors"])


@router.post("/add_sensor/")
async def add_sensor_details(sensor: SensorDetails):
    query = sensor_details_table.insert().values(
        sensor_name=sensor.sensor_name,
        units_short=sensor.units_short,
        units_long=sensor.units_long
    )
    result = con.execute(query)
    return {"inserted_at": result.inserted_primary_key}
