from abc import ABC, abstractmethod
from pathlib import Path


class DocumentExtractor(ABC):

    @abstractmethod
    def extract_text(
        self,
        file_path: Path,
    ) -> str:
        # Extract text from a document.
        raise NotImplementedError