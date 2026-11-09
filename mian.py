from contextlib import asynccontextmanager

from fastapi import FastAPI

from Routes.auth_routes import router as auth_router
from Routes.task_routes import router as task_router
from Routes.user_auth import router as user_router
from database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Task Management API", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)


@app.get("/")
async def home():
    return {"message": "Welcome to the Task Management API"}
