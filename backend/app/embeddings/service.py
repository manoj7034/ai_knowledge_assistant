from app.embeddings.factory import EmbeddingProviderFactory


class EmbeddingService:

    def __init__(self):
        self.provider = (
            EmbeddingProviderFactory.get_provider()
        )

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return self.provider.embed(texts)