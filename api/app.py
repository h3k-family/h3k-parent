from fastapi import FastAPI
from auth import auth
from sensors import routes as sensor_routes


app = FastAPI(
    title="h3k-child API",
    description="Haba na haba, hujaza kibaba. Part of the h3k project.",
    version="0.0.1",
)

app.include_router(auth.router)
app.include_router(sensor_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
