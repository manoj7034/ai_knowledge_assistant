from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import ProcessingStatus


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    original_filename: str
    content_type: str
    file_size: int
    processing_status: ProcessingStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }