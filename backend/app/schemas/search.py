from pydantic import BaseModel


class SearchResult(BaseModel):
    id: str
    distance: float
    properties: dict


class SearchResponse(BaseModel):
    results: list[SearchResult]