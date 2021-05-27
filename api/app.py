from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/")
async def read_items(token: str = Depends(ouath2_scheme)):
    return {"token": token}
