from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    # Abstract base class for embedding providers.

    @abstractmethod
    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        # Generate embeddings for the supplied texts..
        
        raise NotImplementedError