from app.database.base import Base
from app.database.mixins import (
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


class BaseModel(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    # Base class inherited by all database models.

    __abstract__ = True