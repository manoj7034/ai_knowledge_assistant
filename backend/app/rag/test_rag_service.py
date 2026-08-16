from app.llms.factory import LLMProviderFactory
from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import RAGPromptBuilder
from app.services.rag_service import RAGService


def main():

    llm = LLMProviderFactory.get_provider()

    rag_service = RAGService(
        llm=llm,
        context_builder=ContextBuilder(),
        prompt_builder=RAGPromptBuilder(),
    )

    documents = [
        {
            "chunk_id": "chunk-1",
            "filename": "FastAPI_Guide.pdf",
            "chunk_index": 0,
            "content": (
                "FastAPI is a modern Python web framework "
                "for building APIs."
            ),
            "rerank_score": 7.5,
        },
        {
            "chunk_id": "chunk-2",
            "filename": "FastAPI_Guide.pdf",
            "chunk_index": 1,
            "content": (
                "FastAPI supports dependency injection "
                "for managing dependencies."
            ),
            "rerank_score": 6.8,
        },
    ]

    answer = rag_service.generate_answer(
        query="What is FastAPI?",
        documents=documents,
    )

    print("\n========== RAG ANSWER ==========\n")
    print(answer)


if __name__ == "__main__":
    main()