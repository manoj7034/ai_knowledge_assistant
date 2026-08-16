import copy
from copy import deepcopy
from sentence_transformers import CrossEncoder


class CrossEncoderService:

    def __init__(self):
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        limit: int | None = None,
    ) -> list[dict]:

        if not documents:
            return []

        reranked_documents = deepcopy(documents)

        pairs = [
            (query, doc["content"])
            for doc in reranked_documents
        ]

        scores = self.model.predict(pairs)

        for doc, score in zip(reranked_documents, scores):
            doc["rerank_score"] = float(score)

        reranked_documents.sort(
            key=lambda x: x["rerank_score"],
            reverse=True,
        )

        if limit is not None:
            reranked_documents = reranked_documents[:limit]

        return reranked_documents