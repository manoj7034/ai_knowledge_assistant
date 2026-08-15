from typing import Any
import re

from sklearn.metrics.pairwise import cosine_similarity

from app.chunking.base import TextChunker
from app.config.settings import settings
from app.embeddings.service import EmbeddingService


class SemanticChunker(TextChunker):
    """
    Semantic chunking using sentence embeddings.

    Workflow:
        1. Split text into sentences.
        2. Generate embeddings using the shared EmbeddingService.
        3. Compute cosine similarity between adjacent sentences.
        4. Create a new chunk when similarity falls below the threshold.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        similarity_threshold: float = settings.SEMANTIC_CHUNK_THRESHOLD,
    ):
        self.embedding_service = embedding_service
        self.similarity_threshold = similarity_threshold

    def split(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into semantic chunks based on
        similarity between adjacent sentences.
        """

        sentences = self._split_sentences(text)

        if not sentences:
            return []

        if len(sentences) == 1:
            return sentences

        embeddings = self._generate_embeddings(
            sentences,
        )

        similarities = self._calculate_similarities(
            embeddings,
        )

        chunks: list[str] = []

        current_chunk = [sentences[0]]

        for i, similarity in enumerate(similarities):

            if similarity >= self.similarity_threshold:

                current_chunk.append(
                    sentences[i + 1]
                )

            else:

                chunks.append(
                    " ".join(current_chunk)
                )

                current_chunk = [
                    sentences[i + 1]
                ]

        if current_chunk:
            chunks.append(
                " ".join(current_chunk)
            )

        return chunks

    def _split_sentences(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into individual sentences.
        """

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    def _generate_embeddings(
        self,
        sentences: list[str],
    ) -> list[list[float]]:
        """
        Generate normalized sentence embeddings
        using the shared EmbeddingService.
        """

        return self.embedding_service.generate_embeddings(
            sentences,
        )

    def _calculate_similarities(
        self,
        embeddings: Any,
    ) -> list[float]:
        """
        Calculate cosine similarity between
        adjacent sentence embeddings.
        """

        similarities: list[float] = []

        for i in range(len(embeddings) - 1):

            similarity = cosine_similarity(
                [embeddings[i]],  # type: ignore
                [embeddings[i + 1]],  # type: ignore
            )[0][0]

            similarities.append(
                float(similarity)
            )

        return similarities