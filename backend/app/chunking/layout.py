import re

from app.chunking.base import TextChunker
from app.config.settings import settings


class LayoutAwareChunker(TextChunker):
    """
    Layout-aware chunker.

    Uses document structure such as:

    - Page boundaries
    - Markdown-style headings
    - Numbered headings
    - Paragraph boundaries

    The goal is to preserve logical sections instead of
    blindly splitting text based only on character count.
    """

    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(
        self,
        text: str,
    ) -> list[str]:

        if not text.strip():
            return []

        blocks = self._extract_blocks(text)

        chunks: list[str] = []

        current_section: list[str] = []

        for block in blocks:

            if self._is_heading(block):

                if current_section:
                    chunks.extend(
                        self._split_section(
                            current_section
                        )
                    )

                current_section = [block]

            else:

                current_section.append(block)

        if current_section:

            chunks.extend(
                self._split_section(
                    current_section
                )
            )

        return chunks

    def _extract_blocks(
        self,
        text: str,
    ) -> list[str]:
        """
        Extract logical blocks from the document.

        Blocks are separated by blank lines.
        """

        raw_blocks = re.split(
            r"\n\s*\n",
            text,
        )

        return [
            block.strip()
            for block in raw_blocks
            if block.strip()
        ]

    def _is_heading(
        self,
        block: str,
    ) -> bool:
        """
        Detect common heading patterns.

        Supports:

        # Heading
        ## Heading
        1. Introduction
        1.1 Authentication
        2. Security
        """

        first_line = block.splitlines()[0].strip()

        # Markdown heading
        if re.match(
            r"^#{1,6}\s+.+",
            first_line,
        ):
            return True

        # Numbered heading
        if re.match(
            r"^\d+(\.\d+)*[\.\)]?\s+[A-Z].*",
            first_line,
        ):
            return True

        return False

    def _split_section(
        self,
        blocks: list[str],
    ) -> list[str]:
        """
        Keep a heading with its related content while
        respecting the configured chunk size.
        """

        chunks: list[str] = []

        current_chunk = ""

        for block in blocks:

            if not current_chunk:

                current_chunk = block
                continue

            candidate = (
                f"{current_chunk}\n\n{block}"
            )

            if len(candidate) <= self.chunk_size:

                current_chunk = candidate

            else:

                chunks.append(
                    current_chunk
                )

                current_chunk = block

        if current_chunk:

            chunks.append(
                current_chunk
            )

        return chunks