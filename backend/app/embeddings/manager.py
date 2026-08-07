from app.embeddings.service import EmbeddingService


_embedding_service: EmbeddingService | None = None


def initialize_embedding_service() -> None:
    global _embedding_service

    if _embedding_service is None:
        print("Loading embedding model...")
        _embedding_service = EmbeddingService()
        print("Embedding model loaded.")


def get_embedding_service() -> EmbeddingService:
    if _embedding_service is None:
        raise RuntimeError(
            "EmbeddingService has not been initialized."
        )

    return _embedding_service