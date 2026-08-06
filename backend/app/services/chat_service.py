from app.embeddings.service import EmbeddingService
from app.llms.base import LLMProvider
from app.prompts.rag_prompt import build_rag_prompt
from app.vectorstores.weaviate_store import WeaviateStore


class ChatService:

    def __init__(
        self,
        *,
        embedding_service: EmbeddingService,
        vector_store: WeaviateStore,
        llm: LLMProvider,
    ):

        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm = llm

    def ask(
        self,
        *,
        question: str,
        owner_id: str,
    ) -> dict:

        query_vector = self.embedding_service.generate_embeddings(
            [question],
            )[0]

        results = self.vector_store.semantic_search(
            query_vector=query_vector, 
            owner_id=owner_id,
            )

        if not results:
            return {
                "answer": "I couldn't find anything relevant in your documents.", 
                "sources": [],
                }

        prompt = build_rag_prompt(
            question=question, 
            contexts=results,
            )

        answer = self.llm.generate(
            prompt=prompt,
            )

        sources = [
            {
                "document_id": str(item["document_id"]),
                "filename": item["filename"],
                "chunk_index": item["chunk_index"],
                "score": item["score"],
            }
            for item in results
        ]

        return {
        "answer": answer,
        "sources": sources,
        }