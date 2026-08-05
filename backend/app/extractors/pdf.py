import fitz
from pathlib import Path
from app.extractors.base import DocumentExtractor


class PDFExtractor(DocumentExtractor):

    def extract_text(
        self,
        file_path: Path,
    ) -> str:

        document = fitz.open(file_path)

        try:
            pages = []

            for page in document:
                pages.append(page.get_text())

            return "\n".join(pages)

        finally:
            document.close()