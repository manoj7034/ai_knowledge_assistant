from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.service import AuthenticationService
from app.dependencies.database import get_db
from app.dependencies.storage import get_storage_provider
from app.embeddings.service import EmbeddingService
from app.services.document_processing_service import DocumentProcessingService
from app.services.document_service import DocumentService
from app.storage.base import StorageProvider
from app.vectorstores.weaviate_store import WeaviateStore
from app.services.search_service import SearchService
from app.llms.factory import LLMProviderFactory
from app.services.chat_service import ChatService


def get_authentication_service(
    db: Session = Depends(get_db),
) -> AuthenticationService:
    return AuthenticationService(db)


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


def get_vector_store():
    store = WeaviateStore()

    try:
        yield store

    finally:
        store.close()


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
        vector_store: WeaviateStore = Depends(get_vector_store),
        ) -> SearchService:

    return SearchService(
        embedding_service=EmbeddingService(),
        vector_store=vector_store,
    )


def get_chat_service(
        vector_store: WeaviateStore = Depends(get_vector_store),
        ) -> ChatService:

    return ChatService(
        embedding_service=EmbeddingService(),
        vector_store=vector_store,
        llm=LLMProviderFactory.get_provider(),
    )