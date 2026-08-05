import shutil
from fastapi import APIRouter, Depends, File, UploadFile, status
from pathlib import Path
from tempfile import NamedTemporaryFile
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.dependencies.services import get_document_service
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):
    with NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file,)
        # temp_file.write(file.file.read())
        temp_path = Path(temp_file.name)

    try:
        document = service.upload_document(
        owner=current_user,
        file_path=temp_path,
        original_filename=file.filename or "document",
        content_type=file.content_type or "application/octet-stream",
        file_size=temp_path.stat().st_size,
        )

        return document

    finally:

        file.file.close()

        if temp_path.exists():
            temp_path.unlink()


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents(
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):

    return service.list_documents(current_user)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):

    return service.get_document(
        current_user,
        document_id,
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):

    service.delete_document(
        current_user,
        document_id,
    )