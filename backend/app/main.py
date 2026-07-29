from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.api.v1.router import api_router
from app.exceptions.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the application starts and once when it shuts down.
    print("Starting Enterprise AI Platform...")

    yield
    print("Shutting down Enterprise AI Platform...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise AI Knowledge Platform",
    lifespan=lifespan 
)


register_exception_handlers(app)



@app.get("/health", tags=["Health"])
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