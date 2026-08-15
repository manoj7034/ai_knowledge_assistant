from pathlib import Path

from sqlalchemy.orm import Session

from app.chunking.factory import ChunkerFactory
from app.core.logging import logger
from app.embeddings.service import EmbeddingService
from app.extractors.factory import ExtractorFactory
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.enums import ProcessingStatus
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.vectorstores.weaviate_store import WeaviateStore


class DocumentProcessingService:

    def __init__(
        self,
        db: Session,
        embedding_service: EmbeddingService,
        vector_store: WeaviateStore,
    ):
        self.db = db

        self.embedding_service = embedding_service
        self.vector_store = vector_store

        self.document_repository = DocumentRepository(db)
        self.chunk_repository = DocumentChunkRepository(db)

        self.chunker = ChunkerFactory.get_chunker(
            embedding_service=self.embedding_service
        )

    def process_document(
        self,
        document: Document,
    ) -> None:

        try:

            logger.info(
                "Processing document %s",
                document.id,
            )

            self.document_repository.update_status(
                document,
                ProcessingStatus.PROCESSING,
            )

            self.db.commit()

            file_path = Path(document.storage_path)

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

            chunks = self.chunker.split(text)

            if not chunks:
                raise ValueError(
                    "No chunks were generated."
                )

            logger.info(
                "Generated %d chunks.",
                len(chunks),
            )

            entities = self._build_chunk_entities(
                document,
                chunks,
            )

            #
            # Save chunks into PostgreSQL first
            #

            for entity in entities:
                self.chunk_repository.save(entity)

            self.db.commit()

            for entity in entities:
                self.db.refresh(entity)

            #
            # Generate embeddings
            #

            texts = [
                entity.content
                for entity in entities
            ]

            vectors = self.embedding_service.generate_embeddings(
                texts,
            )

            #
            # Index into Weaviate
            #

            self.vector_store.index_chunks(
                document=document,
                chunks=entities,
                vectors=vectors,
            )

            self.document_repository.update_status(
                document,
                ProcessingStatus.COMPLETED,
            )

            self.db.commit()

            logger.info(
                "Document %s processed successfully.",
                document.id,
            )

        except Exception:

            logger.exception(
                "Failed to process document %s",
                document.id,
            )

            self.db.rollback()

            failed_document = self.document_repository.get_by_id(
                document.id,
            )

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
                chunk_metadata=None,
            )
            for index, chunk in enumerate(chunks)
        ]