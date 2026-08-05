from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.service import AuthenticationService
from app.dependencies.database import get_db
from app.dependencies.storage import get_storage_provider
from app.services.document_service import DocumentService


def get_authentication_service(db: Session = Depends(get_db),) -> AuthenticationService:
    return AuthenticationService(db)


def get_document_service(
    db: Session = Depends(get_db),
    storage = Depends(get_storage_provider),
) -> DocumentService:

    return DocumentService(
        db=db,
        storage=storage,
    )