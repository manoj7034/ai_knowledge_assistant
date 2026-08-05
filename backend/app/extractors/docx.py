from pathlib import Path
from docx import Document

from app.extractors.base import DocumentExtractor


class DOCXExtractor(DocumentExtractor):

    def extract_text(
        self,
        file_path: Path,
    ) -> str:

        document = Document(file_path) # type: ignore

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )