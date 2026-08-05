from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.repositories.base import BaseRepository


class DocumentChunkRepository(
    BaseRepository[DocumentChunk],
):

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(
            db,
            DocumentChunk,
        )

    def get_by_document(
        self,
        document_id: UUID,
    ) -> list[DocumentChunk]:

        stmt = (
            select(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.chunk_index
            )
        )

        return list(
            self.db.scalars(stmt).all()
        )