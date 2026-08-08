from fastapi import Request

from app.embeddings.service import EmbeddingService
from app.llms.base import LLMProvider
from app.vectorstores.weaviate_store import WeaviateStore
from app.rerankers.service import CrossEncoderService
from app.compression.service import ContextCompressionService


def get_embedding_service(
    request: Request,
) -> EmbeddingService:

    return request.app.state.embedding_service


def get_vector_store(
    request: Request,
) -> WeaviateStore:

    return request.app.state.vector_store


def get_reranker(
    request: Request,
) -> CrossEncoderService:

    return request.app.state.reranker


def get_compressor(
    request: Request,
) -> ContextCompressionService:

    return request.app.state.compressor


def get_llm(
    request: Request,
) -> LLMProvider:

    return request.app.state.llm