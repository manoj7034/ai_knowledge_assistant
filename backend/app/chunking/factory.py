from app.chunking.base import TextChunker
from app.chunking.recursive import RecursiveChunker
from app.chunking.semantic import SemanticChunker
from app.config.settings import settings

from app.config.settings import settings


class ChunkerFactory:

    @staticmethod
    def get_chunker(
        strategy: str = "recursive",
    ) -> TextChunker:

        strategy = strategy.lower()

        chunker = ChunkerFactory.get_chunker(
    settings.CHUNKING_STRATEGY
)

        if strategy == "recursive":
            return RecursiveChunker(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
            )

        elif strategy == "semantic":
            return SemanticChunker()

        raise ValueError(
            f"Unsupported chunking strategy: {strategy}"
        )