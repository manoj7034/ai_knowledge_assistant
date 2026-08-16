from typing import Any


class ContextBuilder:
    """
    Builds a clean textual context from compressed
    retrieval results for the LLM.
    """

    def build(
            self,
            documents: list[dict[str, Any]],
    ) -> str:

        if not documents:
            return ""

        context_parts: list[str] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):

            filename = document.get(
                "filename",
                "Unknown source",
            )

            chunk_index = document.get(
                "chunk_index",
                "Unknown",
            )

            content = document.get(
                "content",
                "",
            ).strip()

            if not content:
                continue

            context_parts.append(
                f"""[Source {index}]
File: {filename}
Chunk: {chunk_index}

{content}
"""
            )

        return "\n".join(context_parts)

