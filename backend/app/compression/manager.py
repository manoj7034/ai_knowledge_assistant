from app.compression.service import ContextCompressionService

_compressor: ContextCompressionService | None = None


def initialize_compressor() -> None:
    global _compressor

    if _compressor is None:
        print("Initializing Context Compressor...")
        _compressor = ContextCompressionService()
        print("Context Compressor ready.")


def get_compressor() -> ContextCompressionService:
    if _compressor is None:
        raise RuntimeError(
            "ContextCompressionService not initialized."
        )

    return _compressor


def shutdown_compressor() -> None:
    global _compressor
    _compressor = None