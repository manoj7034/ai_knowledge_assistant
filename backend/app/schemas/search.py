from uuid import UUID
from pydantic import BaseModel


class SearchResult(BaseModel):
    chunk_id: str
    document_id: UUID
    filename: str
    content: str
    chunk_index: int
    content_type: str
    score: float


class SearchFilters(BaseModel):
    document_id: UUID | None = None
    content_type: str | None = None
    filename: str | None = None


class FusionSearchResult(SearchResult):
    rrf_score: float


class RerankedSearchResult(FusionSearchResult):
    rerank_score: float


class HybridSearchResponse(BaseModel):
    semantic: list[SearchResult]
    keyword: list[SearchResult]
    fusion: list[FusionSearchResult]
    reranked: list[RerankedSearchResult]
    compressed: list[RerankedSearchResult]


