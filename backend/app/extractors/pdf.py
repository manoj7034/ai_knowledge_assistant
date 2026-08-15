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

            for page_number, page in enumerate(
                document,
                start=1,
            ):

                page_text = page.get_text()

                if not page_text.strip():
                    continue

                pages.append(
                    f"\n[PAGE {page_number}]\n"
                    f"{page_text.strip()}\n"
                )

            return "\n".join(pages)

        finally:
            document.close()