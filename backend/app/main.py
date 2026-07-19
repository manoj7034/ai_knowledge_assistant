from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.settings import settings


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


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }