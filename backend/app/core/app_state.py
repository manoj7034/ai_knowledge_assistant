from fastapi import FastAPI

from app.embeddings.manager import initialize_embedding_service
from app.vectorstores.manager import initialize_vector_store
from app.llms.manager import initialize_llm
from app.llms.manager import shutdown_llm
from app.vectorstores.manager import shutdown_vector_store
from app.rerankers.manager import initialize_reranker, shutdown_reranker, get_reranker


def initialize_app_state(app: FastAPI) -> None:
    # Initialize shared application resources.

    # These resources are created once during startup and reused throughout the application's lifetime.

    app.state.embedding_service = initialize_embedding_service()

    app.state.vector_store = initialize_vector_store()

    initialize_reranker()
    app.state.reranker = get_reranker()

    app.state.llm = initialize_llm()


def shutdown_app_state(app: FastAPI) -> None:
    # Cleanly release shared resources.

    shutdown_vector_store()

    shutdown_reranker()

    shutdown_llm()