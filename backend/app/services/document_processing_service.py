from pathlib import Path

from sqlalchemy.orm import Session

from app.chunking.factory import ChunkerFactory
from app.extractors.factory import ExtractorFactory
from app.models.document import Document
from app.models.enums import ProcessingStatus
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.models.document_chunk import DocumentChunk
from app.core.logging import logger


class DocumentProcessingService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.document_repository = DocumentRepository(db)
        self.chunk_repository = DocumentChunkRepository(db)

        self.chunker = ChunkerFactory.get_chunker()

    
    def process_document(self, document: Document,) -> None:

        try:

            logger.info("Processing document %s", document.id,)

            self.document_repository.update_status(
                document,
                ProcessingStatus.PROCESSING,
            )

            self.db.commit()

            file_path = Path(
                document.storage_path,
            )

            extractor = ExtractorFactory.get_extractor(
                file_path,
            )

            text = extractor.extract_text(
                file_path,
            )

            if not text.strip():
                raise ValueError(
                    "Document contains no extractable text."
                )

            chunks = self.chunker.split(
                text,
            )
            if not chunks:
                raise ValueError(
                    "No chunks were generated."
                )

            logger.info("Extracted %d chunks", len(chunks),)

            entities = self._build_chunk_entities(
                document,
                chunks,
            )

            for entity in entities:
                self.chunk_repository.save(entity)

            self.document_repository.update_status(
                document,
                ProcessingStatus.COMPLETED,
            )

            logger.info("Document processing completed",)

            self.db.commit()

        except Exception:

            self.db.rollback()

            failed_document = self.document_repository.get_by_id(
                document.id,)

            if failed_document is not None:
                self.document_repository.update_status(
                    failed_document, 
                    ProcessingStatus.FAILED,
                    )

                self.db.commit()

            raise


    def _build_chunk_entities(
            self, 
            document: Document, 
            chunks: list[str],
            ) -> list[DocumentChunk]:

        return [
            DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            content=chunk,
            page_number=None,
            token_count=None,
            metadata=None,
        )

        for index, chunk in enumerate(chunks)
        ]