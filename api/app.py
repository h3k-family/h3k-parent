import os
from fastapi import FastAPI
from auth import auth

app = FastAPI(
    title="h3k-child API",
    description="Haba na haba, hujaza kibaba. Part of the h3k project.",
    version="0.0.1",
)

app.include_router(auth.router)


@app.get("/")
async def root():
    test_var = os.getenv("TEST_VAR")
    test_var = test_var if test_var else "such empty :("
    return {"message": "Hello World: " + test_var}
