from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.config.settings import settings


metadata = MetaData(schema=settings.DB_SCHEMA)


class Base(DeclarativeBase):
    # Base class for all SQLAlchemy models
    metadata = metadata
    