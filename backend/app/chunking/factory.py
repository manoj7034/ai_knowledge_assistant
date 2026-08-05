from app.chunking.base import TextChunker
from app.chunking.recursive import RecursiveChunker
from app.config.settings import settings


class ChunkerFactory:

    @staticmethod
    def get_chunker() -> TextChunker:
        return RecursiveChunker(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )