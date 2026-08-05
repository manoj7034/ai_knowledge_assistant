from app.embeddings.service import EmbeddingService
from app.vectorstores.weaviate_store import WeaviateStore


class SearchService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: WeaviateStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def search(
        self,
        *,
        query: str,
        owner_id: str,
        limit: int = 5,
    ):

        vector = self.embedding_service.generate_embeddings(
            [query]
        )[0]

        return self.vector_store.search(
            query_vector=vector,
            owner_id=owner_id,
            limit=limit,
        )