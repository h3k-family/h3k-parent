from fastapi import APIRouter, Depends
from api.models import con
from auth.auth import get_current_active_user
from auth.models import User
from .models import sensor_details_table, SensorDetails


router = APIRouter(tags=["sensors"])


@router.post("/add_sensor/")
async def add_sensor_details(sensor: SensorDetails,
                             current_user: User = Depends(get_current_active_user)):
    query = sensor_details_table.insert().values(
        sensor_name=sensor.sensor_name,
        owner=current_user.id,
        units_short=sensor.units_short,
        units_long=sensor.units_long
    )
    result = con.execute(query)
    return {"inserted_at": result.inserted_primary_key}
