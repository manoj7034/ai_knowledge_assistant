from pydantic import BaseModel
from uuid import UUID


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    document_id: UUID
    filename: str
    chunk_index: int
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


