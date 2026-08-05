from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories.base import BaseRepository
from app.models.enums import ProcessingStatus


class DocumentRepository(BaseRepository[Document]):

    def __init__(self, db: Session,):
        super().__init__(db, Document,)

    def get_by_owner(self, owner_id: UUID) -> list[Document]:
        stmt = (
            select(Document).where(
                Document.owner_id == owner_id
            )
        )

        return list(self.db.scalars(stmt).all())

    def get_by_id_and_owner(self, document_id:UUID, owner_id: UUID) -> Document | None:
        stmt = (
            select(Document)
            .where(
                Document.id == document_id,
                Document.owner_id == owner_id,
            )
        )

        return self.db.scalar(stmt)

    def get_pending_documents(
        self,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .where(
                Document.processing_status == ProcessingStatus.PENDING
            )
            .order_by(Document.created_at.asc())
        )

        return list(self.db.scalars(stmt).all())

    def get_processing_documents(
        self,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .where(
                Document.processing_status == ProcessingStatus.PROCESSING
            )
            .order_by(Document.created_at.asc())
        )

        return list(self.db.scalars(stmt).all())

    def update_status(
        self,
        document: Document,
        status: ProcessingStatus,
    ) -> Document:
        document.processing_status = status

        self.db.flush()
        self.db.refresh(document)

        return document

    def search_by_filename(
        self,
        owner_id: UUID,
        filename: str,
    ) -> list[Document]:
        stmt = (
            select(Document)
            .where(
                Document.owner_id == owner_id,
                Document.original_filename.ilike(f"%{filename}%"),
            )
            .order_by(Document.created_at.desc())
        )

        return list(self.db.scalars(stmt).all())

    # def count_by_owner(
    #     self,
    #     owner_id: UUID,
    # ) -> int:
    #     return len(self.get_by_owner(owner_id))