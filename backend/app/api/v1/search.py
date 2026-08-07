from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_search_service
from app.models.user import User
from app.schemas.search import HybridSearchResponse
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
    service: SearchService = Depends(get_search_service),
    current_user: User = Depends(get_current_user),
):
    return service.search(
        query=query,
        owner_id=str(current_user.id),
    )