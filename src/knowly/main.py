
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from src.knowly.api.routes.health import router as health_router
from src.knowly.core.config import settings
from src.knowly.db.session import engine
from src.knowly.db.init_db import init_db



@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    Path("storage").mkdir(
        parents=True,
        exist_ok=True,
    )

    # Verify database connectivity during startup
    await init_db()

    print("Database initialized successfully.")
    print("Knowly application started successfully.")

    yield

    # Shutdown
    await engine.dispose()

    print("Knowly application shut down.")


app = FastAPI(
    title=settings.APP_NAME,
    description="A production-oriented RAG system with hybrid retrieval.",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(
    health_router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Knowly",
        "status": "running",
    }
