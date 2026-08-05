from pathlib import Path

from app.extractors.base import DocumentExtractor
from app.extractors.pdf import PDFExtractor
from app.extractors.txt import TXTExtractor
from app.extractors.docx import DOCXExtractor


class ExtractorFactory:

    _extractors = {
        ".pdf": PDFExtractor(),
        ".txt": TXTExtractor(),
        ".docx": DOCXExtractor(),
    }

    @classmethod
    def get_extractor(
        cls,
        file_path: Path,
    ) -> DocumentExtractor:

        extension = file_path.suffix.lower()

        extractor = cls._extractors.get(extension)

        if extractor is None:
            raise ValueError(
                f"No extractor available for {extension}"
            )

        return extractor