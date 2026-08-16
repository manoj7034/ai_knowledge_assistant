from typing import Any
from app.config.settings import settings


class ContextCompressionService:
    # Removes low-quality retrieved chunks before sending them to the LLM.

    def compress(
        self,
        documents: list[dict[str, Any]],
        *,
        threshold: float | None = None,
    ) -> list[dict]:

        if not documents:
            return []

        if threshold is None:
            threshold = settings.RERANK_SCORE_THRESHOLD

        documents = sorted(
            documents,
            key=lambda x: x.get("rerank_score", float("-inf")),
            reverse=True,
        )

        return [
            doc
            for doc in documents
            if doc.get("rerank_score", float("-inf")) >= threshold
        ]