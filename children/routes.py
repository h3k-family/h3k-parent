from fastapi import APIRouter, Depends
from sqlalchemy import exc
import sqlalchemy as sa
from api.models import con
from auth.auth import get_current_active_user
from auth.models import DbUser, user_table
from .models import children_table, Child

router = APIRouter(prefix="/children", tags=["sensors"])


@router.post("/add/")
async def add_sensor_details(child: Child,
                             _current_user: DbUser = Depends(get_current_active_user)):
    query = children_table.insert().values(
        url=child.url,
    )
    try:
        result = con.execute(query)
    except exc.SQLAlchemyError:
        return {"error": "could not save record"}

    return {"inserted_at": result.inserted_primary_key}
