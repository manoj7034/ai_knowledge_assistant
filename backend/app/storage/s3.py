from pathlib import Path

from app.storage.base import StorageProvider


class S3Storage(StorageProvider):

    def save(
        self,
        file_path: Path,
        destination: str,
    ) -> str:
        raise NotImplementedError

    def delete(
        self,
        storage_path: str,
    ) -> None:
        raise NotImplementedError

    def exists(
        self,
        storage_path: str,
    ) -> bool:
        raise NotImplementedError