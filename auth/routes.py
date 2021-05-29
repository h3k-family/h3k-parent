from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.models import con
import auth.models as mo
from .auth import ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
from .auth import create_access_token, authenticate_user

router = APIRouter()


@router.post("/token", tags=["auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        mo.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", tags=["auth"])
async def read_users_me(current_user: mo.User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/", tags=["auth"])
async def read_own_items(current_user: mo.User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/users/add/", tags=["auth"])
async def create_user(user: mo.UserInDB):
    query = mo.user_table.insert().values(
        username=user.username,
        email=user.email,
        password=user.hashed_password,
        disabled=user.disabled
    )
    result = con.execute(query)
    return {"inserted_at": result.inserted_primary_key}
