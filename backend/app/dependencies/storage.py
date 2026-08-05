from pathlib import Path

from app.config.settings import settings
from app.storage.base import StorageProvider
from app.storage.local import LocalStorage


def get_storage_provider() -> StorageProvider:

    if settings.STORAGE_PROVIDER == "local":
        return LocalStorage(
            Path(settings.LOCAL_STORAGE_PATH)
        )

    raise ValueError(
        f"Unsupported storage provider: {settings.STORAGE_PROVIDER}"
    )