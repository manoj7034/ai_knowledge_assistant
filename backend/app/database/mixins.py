import uuid

from datetime import datetime, UTC

from sqlalchemy import DateTime, func
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    # Adds created_at and updated_at timestamps to all models.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class UUIDPrimaryKeyMixin:
    # Adds a UUID primary key to every table.

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


