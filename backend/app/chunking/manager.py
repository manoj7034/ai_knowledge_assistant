from app.chunking.base import TextChunker
from app.chunking.factory import ChunkerFactory
from app.config.settings import settings

_chunker: TextChunker | None = None


def initialize_chunker() -> None:
    global _chunker

    if _chunker is None:
        print("Loading Chunker...")

        _chunker = ChunkerFactory.get_chunker(
            settings.CHUNKING_STRATEGY,
        )

        print("Chunker loaded.")


def get_chunker() -> TextChunker:
    if _chunker is None:
        raise RuntimeError("Chunker has not been initialized.")

    return _chunker


def shutdown_chunker() -> None:
    global _chunker
    _chunker = None