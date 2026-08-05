from typing import TYPE_CHECKING
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.models.enums import ProcessingStatus

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document_chunk import DocumentChunk


class Document(BaseModel):
    __tablename__ = "documents"

    owner_id: Mapped[str] = mapped_column(
        ForeignKey(
            "enterprise_ai.users.id",
            ondelete="CASCADE",
            ),
            nullable=False,
        )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        Enum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        back_populates = "documents",
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan"
    )
