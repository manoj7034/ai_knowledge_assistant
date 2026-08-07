from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.service import AuthenticationService
from app.dependencies.database import get_db
from app.dependencies.storage import get_storage_provider
from app.services.document_processing_service import DocumentProcessingService
from app.services.document_service import DocumentService
from app.storage.base import StorageProvider
from app.services.search_service import SearchService
from app.services.chat_service import ChatService
from app.embeddings.manager import get_embedding_service
from app.vectorstores.manager import get_vector_store
from app.llms.manager import get_llm


def get_authentication_service(
    db: Session = Depends(get_db),
) -> AuthenticationService:
    return AuthenticationService(db)


# def get_embedding_service() -> EmbeddingService:
#     return EmbeddingService()


# def get_vector_store():
#     store = WeaviateStore()

#     try:
#         yield store

#     finally:
#         store.close()


def get_document_processing_service(
    db: Session = Depends(get_db),
) -> DocumentProcessingService:

    return DocumentProcessingService(
        db=db,
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
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


def get_search_service() -> SearchService:

    return SearchService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )


def get_chat_service() -> ChatService:

    return ChatService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
        llm=get_llm(),
    )