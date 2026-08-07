from app.vectorstores.weaviate_store import WeaviateStore


_vector_store: WeaviateStore | None = None


def initialize_vector_store() -> None:
    global _vector_store

    if _vector_store is None:
        print("Connecting to Weaviate...")
        _vector_store = WeaviateStore()
        _vector_store.create_collection()
        print("Weaviate connected.")


def get_vector_store() -> WeaviateStore:
    if _vector_store is None:
        raise RuntimeError(
            "Vector store has not been initialized."
        )

    return _vector_store


def shutdown_vector_store() -> None:
    global _vector_store

    if _vector_store is not None:
        print("Closing Weaviate...")
        _vector_store.close()
        _vector_store = None