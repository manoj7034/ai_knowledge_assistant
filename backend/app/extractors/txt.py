from pathlib import Path

from app.extractors.base import DocumentExtractor


class TXTExtractor(DocumentExtractor):

    def extract_text(
        self,
        file_path: Path,
    ) -> str:

        return file_path.read_text(
            encoding="utf-8",
        )