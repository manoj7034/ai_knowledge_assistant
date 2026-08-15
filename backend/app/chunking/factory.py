from app.chunking.base import TextChunker
from app.chunking.layout import LayoutAwareChunker
from app.chunking.recursive import RecursiveChunker
from app.chunking.semantic import SemanticChunker
from app.config.settings import settings
from app.embeddings.service import EmbeddingService


class ChunkerFactory:

    @staticmethod
    def get_chunker(
        embedding_service: EmbeddingService,
        strategy: str = settings.CHUNKING_STRATEGY,
    ) -> TextChunker:

        strategy = strategy.lower()

        if strategy == "recursive":

            return RecursiveChunker(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
            )

        if strategy == "semantic":

            return SemanticChunker(
                embedding_service=embedding_service,
            )

        if strategy == "layout":

            return LayoutAwareChunker(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
            )

        raise ValueError(
            f"Unsupported chunking strategy: {strategy}"
        )