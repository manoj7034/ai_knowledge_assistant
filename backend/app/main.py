from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.settings import settings
from app.exceptions.handlers import register_exception_handlers
from app.vectorstores.weaviate_store import WeaviateStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once during application startup
    and once during shutdown.
    """

    print("Starting Enterprise AI Platform...")

    #
    # Initialize Weaviate
    #

    store = WeaviateStore()

    try:
        store.create_collection()
        print("✓ Weaviate collection is ready.")

    finally:
        store.close()

    yield

    print("Shutting down Enterprise AI Platform...")


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