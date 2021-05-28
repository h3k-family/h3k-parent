from fastapi import FastAPI
from auth import auth

# openssl rand -hex 32
SECRET_KEY = "9a4dbb8b7e5eff75422194bf5820b010607e29819520106db6617445c537d800"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

app = FastAPI(
    title="h3k-child API",
    description="Haba na haba, hujaza kibaba. Part of the h3k project.",
    version="0.0.1",
)

app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
