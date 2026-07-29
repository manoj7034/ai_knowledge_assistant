from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.service import AuthenticationService
from app.dependencies.services import get_authentication_service
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
):
    return service.register(user)
    

@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
):
    return service.login(credentials)