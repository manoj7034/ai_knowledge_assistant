from app.config.settings import settings
from app.embeddings.base import EmbeddingProvider
from app.embeddings.local import LocalEmbeddingProvider


class EmbeddingProviderFactory:

    @staticmethod
    def get_provider() -> EmbeddingProvider:

        if settings.EMBEDDING_PROVIDER == "local":
            return LocalEmbeddingProvider(
                settings.EMBEDDING_MODEL,
            )

        raise ValueError(
            f"Unsupported embedding provider: {settings.EMBEDDING_PROVIDER}"
        )