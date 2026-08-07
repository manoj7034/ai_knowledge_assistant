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


class HybridSearchResponse(BaseModel):
    semantic: list[SearchResult]
    keyword: list[SearchResult]
    fusion: list[SearchResult]


class FusionSearchResult(SearchResult):
    rrf_score: float