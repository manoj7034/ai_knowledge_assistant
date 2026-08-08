from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.service import AuthenticationService
from app.dependencies.database import get_db
from app.dependencies.storage import get_storage_provider
from app.embeddings.manager import get_embedding_service
from app.vectorstores.manager import get_vector_store
from app.llms.manager import get_llm
from app.embeddings.service import EmbeddingService
from app.vectorstores.weaviate_store import WeaviateStore
from app.llms.base import LLMProvider
from app.retrieval.rrf import ReciprocalRankFusion
from app.services.chat_service import ChatService
from app.services.document_processing_service import DocumentProcessingService
from app.services.document_service import DocumentService
from app.services.search_service import SearchService
from app.storage.base import StorageProvider
from app.rerankers.service import CrossEncoderService
from app.dependencies.app_state import get_reranker
from app.compression.service import ContextCompressionService
from app.dependencies.app_state import get_compressor


def get_authentication_service(
    db: Session = Depends(get_db),
) -> AuthenticationService:
    return AuthenticationService(db)


def get_rank_fusion() -> ReciprocalRankFusion:
    return ReciprocalRankFusion()


def get_document_processing_service(
    db: Session = Depends(get_db),
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: WeaviateStore = Depends(get_vector_store),
) -> DocumentProcessingService:

    return DocumentProcessingService(
        db=db,
        embedding_service=embedding_service,
        vector_store=vector_store,
    )


def get_document_service(
    db: Session = Depends(get_db),
    storage: StorageProvider = Depends(get_storage_provider),
    processing_service: DocumentProcessingService = Depends(
        get_document_processing_service
    ),
) -> DocumentService:

    return DocumentService(
        db=db,
        storage=storage,
        processing_service=processing_service,
    )


def get_search_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: WeaviateStore = Depends(get_vector_store),
    rank_fusion: ReciprocalRankFusion = Depends(get_rank_fusion),
    reranker: CrossEncoderService = Depends(get_reranker),
    compressor: ContextCompressionService = Depends(get_compressor),
) -> SearchService:

    return SearchService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        rank_fusion=rank_fusion,
        reranker=reranker,
        compressor=compressor
    )


def get_chat_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: WeaviateStore = Depends(get_vector_store),
    llm: LLMProvider = Depends(get_llm),
) -> ChatService:

    return ChatService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        llm=llm,
    )