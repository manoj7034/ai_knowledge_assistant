from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.settings import settings
from app.core.app_state import (
    initialize_app_state,
    shutdown_app_state,
)
from app.exceptions.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once during application startup
    and once during shutdown.
    """

    print("Starting Enterprise AI Platform...")

    initialize_app_state(app)

    print("Enterprise AI Platform is ready.")

    yield

    print("Shutting down Enterprise AI Platform...")

    shutdown_app_state(app)

    print("Resources released.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise AI Knowledge Platform",
    lifespan=lifespan,
)

register_exception_handlers(app)


@app.get(
    "/health",
    tags=["Health"],
)
async def health_check():

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


app.include_router(
    api_router,
    prefix="/api/v1",
)