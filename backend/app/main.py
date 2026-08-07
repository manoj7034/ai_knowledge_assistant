from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.settings import settings
from app.embeddings.manager import initialize_embedding_service
from app.exceptions.handlers import register_exception_handlers
from app.llms.manager import initialize_llm, shutdown_llm
from app.vectorstores.manager import initialize_vector_store, shutdown_vector_store



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once during application startup
    # and once during shutdown.
    

    print("Starting Enterprise AI Platform...")

    # Initialize shared services

    initialize_embedding_service()
    initialize_vector_store()
    initialize_llm()

    print("Enterprise AI Platform is ready.")

    yield

    print("Shutting down Enterprise AI Platform...")

    shutdown_vector_store()
    shutdown_llm()

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