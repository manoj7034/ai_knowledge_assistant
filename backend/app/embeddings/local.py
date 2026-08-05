from sentence_transformers import SentenceTransformer
from app.embeddings.base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):

    def __init__(
        self,
        model_name: str,
    ):
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        vectors = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return vectors.tolist()