from app.llms.base import LLMProvider
from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import RAGPromptBuilder
from app.schemas.search import SearchFilters
from app.services.search_service import SearchService


class ChatService:

    def __init__(
        self,
        *,
        search_service: SearchService,
        llm: LLMProvider,
        context_builder: ContextBuilder,
        prompt_builder: RAGPromptBuilder,
    ):

        self.search_service = search_service
        self.llm = llm
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder

    def ask(
        self,
        *,
        question: str,
        owner_id: str,
        filters: SearchFilters | None = None,
    ) -> dict:

        # Retrieval

        retrieval = self.search_service.search(
            query=question,
            owner_id=owner_id,
            filters=filters,
        )

        compressed_results = retrieval["compressed"]

        # No relevant context

        if not compressed_results:

            return {
                "answer": (
                    "I couldn't find enough relevant "
                    "information in your documents "
                    "to answer this question."
                ),
                "sources": [],
            }

        # Build Context

        context = self.context_builder.build(
            compressed_results,
        )

        # Build RAG prompt

        prompt = self.prompt_builder.build(
            query=question,
            context=context,
        )

        # Generate answer

        answer = self.llm.generate(prompt)

        # Build sources

        sources = [
            {
                "document_id": str(
                    item["document_id"]
                ),
                "filename": item["filename"],
                "chunk_id": item["chunk_id"],
                "chunk_index": int(item["chunk_index"]),
                "score": float(item["rerank_score"]),
            }
            for item in compressed_results
        ]

        return {
            "answer": answer,
            "sources": sources,
        }