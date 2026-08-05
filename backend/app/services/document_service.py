from pathlib import Path
from uuid import uuid4
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.user import User
from app.models.enums import ProcessingStatus
from app.repositories.document import DocumentRepository
from app.services.document_processing_service import DocumentProcessingService
from app.storage.base import StorageProvider
from app.exceptions.document import DocumentNotFoundException


class DocumentService:

    def __init__(
        self,
        db: Session,
        storage: StorageProvider,
        processing_service: DocumentProcessingService,
    ):
        self.db = db

        self.repository = DocumentRepository(db)

        self.storage = storage
        self.processing_service = processing_service

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
            original_filename,
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
            processing_status=ProcessingStatus.PENDING,
        )

        self.repository.save(document)

        self.db.commit()
        self.db.refresh(document)

        #
        # Process the document
        #

        self.processing_service.process_document(
            document,
        )

        return document

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

        document = self.repository.get_by_id_and_owner(
            document_id,
            owner.id,
        )

        if document is None:
            raise DocumentNotFoundException()

        if self.storage.exists(document.storage_path):
            self.storage.delete(document.storage_path)

        self.repository.delete(document)

        self.db.commit()