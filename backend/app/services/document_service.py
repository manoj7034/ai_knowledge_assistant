from pathlib import Path
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.exceptions.document import DocumentNotFoundException
from app.models.document import Document
from app.models.user import User
from app.repositories.document import DocumentRepository
from app.storage.base import StorageProvider
from app.services.document_processing_service import DocumentProcessingService


class DocumentService:

    def __init__(
        self,
        db: Session,
        storage: StorageProvider,
    ):
        self.db = db
        self.repository = DocumentRepository(db)
        self.storage = storage
        self.processing_service = DocumentProcessingService(db)

    # -------------------------------------------------------------------------
    # Private Helpers
    # -------------------------------------------------------------------------

    def _generate_filename(
        self,
        original_filename: str,
    ) -> str:
        extension = Path(original_filename).suffix
        return f"{uuid4()}{extension}"

    def _build_storage_path(
        self,
        owner: User,
        filename: str,
    ) -> str:
        return f"{owner.id}/{filename}"

    # -------------------------------------------------------------------------
    # Public Methods
    # -------------------------------------------------------------------------

    def upload_document(
        self,
        *,
        owner: User,
        file_path: Path,
        original_filename: str,
        content_type: str,
        file_size: int,
    ) -> Document:

        generated_filename = self._generate_filename(
            original_filename
        )

        storage_path = self._build_storage_path(
            owner,
            generated_filename,
        )

        saved_path = self.storage.save(
            file_path,
            storage_path,
        )

        document = Document(
            owner_id=owner.id,
            filename=generated_filename,
            original_filename=original_filename,
            content_type=content_type,
            file_size=file_size,
            storage_path=saved_path,
        )

        try:
            self.repository.save(document)
            self.db.commit()
            self.db.refresh(document)
            self.processing_service.process_document(document)

            return document

        except Exception:
            self.db.rollback()

            self.storage.delete(saved_path) # type: ignore

            raise

    def list_documents(
        self,
        owner: User,
    ) -> list[Document]:

        return self.repository.get_by_owner(
            owner.id,
        )

    def get_document(
        self,
        owner: User,
        document_id: UUID,
    ) -> Document:

        document = self.repository.get_by_id_and_owner(
            document_id,
            owner.id,
        )

        if document is None:
            raise DocumentNotFoundException()

        return document

    def delete_document(
        self,
        owner: User,
        document_id: UUID,
    ) -> None:

        document = self.get_document(
            owner,
            document_id,
        )

        try:
            self.storage.delete(
                document.storage_path, # type: ignore
            )

            self.repository.delete(document)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise