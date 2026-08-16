from app.rag.context_builder import ContextBuilder


def main():

    documents = [
        {
            "chunk_id": "chunk-1",
            "filename": "Python_Interview.pdf",
            "chunk_index": 0,
            "content": (
                "FastAPI is a modern Python web framework."
            ),
            "rerank_score": 7.5,
        },
        {
            "chunk_id": "chunk-2",
            "filename": "FastAPI_Guide.pdf",
            "chunk_index": 2,
            "content": (
                "Dependency Injection allows "
                "dependencies to be provided automatically."
            ),
            "rerank_score": 6.8,
        },
    ]

    builder = ContextBuilder()

    context = builder.build(documents)

    print("\n========== CONTEXT ==========\n")
    print(context)


if __name__ == "__main__":
    main()