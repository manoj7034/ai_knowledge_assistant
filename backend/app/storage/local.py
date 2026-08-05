from pathlib import Path
import shutil

from app.storage.base import StorageProvider


class LocalStorage(StorageProvider):

    def __init__(
        self,
        root_directory: Path,
    ):
        self.root_directory = root_directory

        self.root_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        file_path: Path,
        destination: str,
    ) -> str:

        destination_path = (
            self.root_directory / destination
        )

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            file_path,
            destination_path,
        )

        return str(destination_path)

    def delete(
        self,
        storage_path: str,
    ) -> None:

        path = Path(storage_path)

        if path.is_file():
            path.unlink()

    def exists(
        self,
        storage_path: str,
    ) -> bool:

        return Path(storage_path).exists()