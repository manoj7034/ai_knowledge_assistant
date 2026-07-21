from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Enterprise AI Platform"
    APP_VERSION: str = "0.1.0"
    APP_ENV : str = "development"
    DEBUG: bool = True

    DATABASE_URL: str
    DB_SCHEMA: str = "enterprise_ai"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()