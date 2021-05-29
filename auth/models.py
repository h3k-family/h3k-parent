from typing import Optional
from pydantic import BaseModel
import sqlalchemy as sa
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class utcnow(expression.FunctionElement):
    type = sa.DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


#  op.create_table(
    #  "users",
    #  sa.Column("id", sa.Integer, primary_key=True),
    #  sa.Column("username", sa.String(100)),
    #  sa.Column("email", sa.String(100)),
    #  sa.Column("password", sa.String(100)),
    #  sa.Column("disabled", sa.Boolean),
    #  sa.Column("updated_at", sa.DateTime,
    #  server_default=utcnow(), server_onupdate=utcnow()),
    #  )
