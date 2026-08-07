from fastapi import Request

from app.embeddings.service import EmbeddingService
from app.llms.base import LLMProvider
from app.vectorstores.weaviate_store import WeaviateStore


def get_embedding_service(
    request: Request,
) -> EmbeddingService:

    return request.app.state.embedding_service


def get_vector_store(
    request: Request,
) -> WeaviateStore:

    return request.app.state.vector_store


def get_llm(
    request: Request,
) -> LLMProvider:

    return request.app.state.llm