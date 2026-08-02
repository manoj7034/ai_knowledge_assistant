from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.service import AuthenticationService
from app.dependencies.services import get_authentication_service
from app.schemas.token import TokenResponse, RefreshTokenRequest, LogoutRequest
from app.schemas.user import UserCreate, UserLogin, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,)
def register(
    user: UserCreate,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
):
    return service.register(user)
    

@router.post("/login", response_model=TokenResponse,)
def login(
    credentials: UserLogin,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
):
    return service.login(credentials)


@router.post("/refresh", response_model=TokenResponse,)
def refresh_token(
    request: RefreshTokenRequest,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
):
    return service.refresh(
        request.refresh_token,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: LogoutRequest,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
):
    service.logout(request)