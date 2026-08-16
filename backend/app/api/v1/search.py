from uuid import UUID
from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_search_service
from app.models.user import User
from app.schemas.search import HybridSearchResponse, SearchFilters
from app.services.search_service import SearchService


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get(
    "",
    response_model=HybridSearchResponse,
)
def semantic_search(
    query: str,
    document_id: UUID | None = None,
    content_type: str | None = None,
    filename: str | None = None,
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user),
):

    filters = SearchFilters(
        document_id=document_id,
        content_type=content_type,
        filename=filename,
    )
    
    return service.search(
        query=query,
        owner_id=str(current_user.id),
        filters=filters,
    )