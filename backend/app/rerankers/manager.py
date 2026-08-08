from app.rerankers.service import CrossEncoderService

_reranker: CrossEncoderService | None = None


def initialize_reranker() -> None:
    """
    Load the Cross Encoder model once during application startup.
    """
    global _reranker

    if _reranker is None:
        print("Loading Cross Encoder...")
        _reranker = CrossEncoderService()
        print("Cross Encoder loaded.")


def get_reranker() -> CrossEncoderService:
    """
    Return the shared Cross Encoder instance.
    """
    if _reranker is None:
        raise RuntimeError(
            "CrossEncoderService has not been initialized."
        )

    return _reranker


def shutdown_reranker() -> None:
    """
    Release the Cross Encoder.
    """
    global _reranker
    _reranker = None