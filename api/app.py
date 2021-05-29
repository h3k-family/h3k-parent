from fastapi import FastAPI
from auth import routes as auth_routes
from children import routes as children_routes


app = FastAPI(
    title="h3k-parent API",
    description="Haba na haba, hujaza kibaba. Part of the h3k project.",
    version="0.0.1",
)

app.include_router(auth_routes.router)
app.include_router(children_routes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
