from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise AI Platform"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str
    DB_SCHEMA: str = "enterprise_ai"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int =7

    STORAGE_PROVIDER: str = "local"
    LOCAL_STORAGE_PATH: str = "./storage"

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    EMBEDDING_PROVIDER: str = "local"
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    WEAVIATE_URL: str = "http://localhost:8080"
    WEAVIATE_API_KEY: str | None = None
    WEAVIATE_COLLECTION: str = "DocumentChunks"
    WEAVIATE_HOST: str = "localhost"
    WEAVIATE_HTTP_PORT: int = 8080
    WEAVIATE_GRPC_PORT: int = 50051


    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings() # type: ignore