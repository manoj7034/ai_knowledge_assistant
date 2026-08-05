from abc import ABC, abstractmethod
from pathlib import Path


class StorageProvider(ABC):

    @abstractmethod
    def save(
        self,
        file_path: Path,
        destination: str,
    ) -> str:
        """Save a file and return its storage path."""
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        storage_path: str,
    ) -> None:
        """Delete a stored file."""
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        storage_path: str,
    ) -> bool:
        """Check whether a file exists."""
        raise NotImplementedError