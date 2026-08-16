from app.embeddings.service import EmbeddingService
from app.vectorstores.weaviate_store import WeaviateStore
from app.retrieval.rrf import ReciprocalRankFusion
from app.rerankers.service import CrossEncoderService
from app.compression.service import ContextCompressionService
from app.schemas.search import SearchFilters
from app.config.settings import settings
from app.core.logging import logger


class SearchService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: WeaviateStore,
        rank_fusion: ReciprocalRankFusion,
        reranker: CrossEncoderService,
        compressor: ContextCompressionService
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.rank_fusion = rank_fusion
        self.reranker = reranker
        self.compressor = compressor

    def search(
        self,
        *,
        query: str,
        owner_id: str,
        filters: SearchFilters | None = None,
    ):

        query_vector = self.embedding_service.generate_embeddings(
            [query],
        )[0]

        filters = filters or SearchFilters()

        semantic_results = self.vector_store.semantic_search(
            query_vector=query_vector,
            owner_id=owner_id,
            limit=settings.SEMANTIC_TOP_K,
            document_id=filters.document_id,
            content_type=filters.content_type,
            filename=filters.filename,
        )

        keyword_results = self.vector_store.keyword_search(
            query=query,
            owner_id=owner_id,
            limit=settings.BM25_TOP_K,
            document_id=filters.document_id,
            content_type=filters.content_type,
            filename=filters.filename,
        )

        fusion_results = self.rank_fusion.fuse(
            semantic_results,
            keyword_results,
            limit=settings.RRF_TOP_K,
        )

        reranked_results = self.reranker.rerank(
            query=query,
            documents=fusion_results,
            limit=settings.RERANK_TOP_K,
        )

        compressed_results = self.compressor.compress(
            reranked_results,
        )

        logger.info(
            "Retrieval counts | semantic=%d keyword=%d fusion=%d reranked=%d compressed=%d",
            len(semantic_results),
            len(keyword_results),
            len(fusion_results),
            len(reranked_results),
            len(compressed_results),
        )
        
        return {
            "semantic": semantic_results,
            "keyword": keyword_results,
            "fusion": fusion_results,
            "reranked": reranked_results,
            "compressed": compressed_results,
        }
    