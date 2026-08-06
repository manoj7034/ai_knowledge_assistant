from pydantic import BaseModel
from uuid import UUID


class SearchResult(BaseModel):
    chunk_id: str
    document_id: UUID
    filename: str
    content: str
    chunk_index: int
    content_type: str
    score: float


class SearchResponse(BaseModel):
    results: list[SearchResult]