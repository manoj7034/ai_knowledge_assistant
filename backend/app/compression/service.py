from typing import Any


class ContextCompressionService:
    # Removes low-quality retrieved chunks before sending them to the LLM.

    def compress(
        self,
        documents: list[dict[str, Any]],
        *,
        threshold: float = 0.0,
    ) -> list[dict]:

        if not documents:
            return []

        documents = sorted(
            documents,
            key=lambda x: x.get("rerank_score", 0),
            reverse=True,
        )

        return [
            doc
            for doc in documents
            if doc.get("rerank_score", float("-inf")) >= threshold
        ]