from app.embeddings.service import EmbeddingService
from app.vectorstores.weaviate_store import WeaviateStore
from app.retrieval.rrf import ReciprocalRankFusion


class SearchService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: WeaviateStore,
        rank_fusion: ReciprocalRankFusion,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.rank_fusion = rank_fusion

    def search(
        self,
        *,
        query: str,
        owner_id: str,
        limit: int = 5,
    ):

        query_vector = self.embedding_service.generate_embeddings(
            [query],
        )[0]

        semantic_results = self.vector_store.semantic_search(
            query_vector=query_vector,
            owner_id=owner_id,
            limit=limit,
        )

        keyword_results = self.vector_store.keyword_search(
            query=query,
            owner_id=owner_id,
            limit=limit,
        )

        fusion_results = self.rank_fusion.fuse(
            semantic_results,
            keyword_results,
        )
        
        return {
            "semantic": semantic_results,
            "keyword": keyword_results,
            "fusion": fusion_results,
        }
    