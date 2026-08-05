from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jose import JWTError, ExpiredSignatureError

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.exceptions.user import InactiveUserException, InsufficientPermissionsException
from app.exceptions.auth import ExpiredAccessTokenException, InvalidAccessTokenException


bearer_scheme  = HTTPBearer(
    auto_error=True,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme ),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
    except ExpiredSignatureError:
        raise ExpiredAccessTokenException()
    except JWTError:
        raise InvalidAccessTokenException()

    subject = payload.get("sub")
    if subject is None:
        raise InvalidAccessTokenException()

    try:
        user_id = UUID(subject)
    except ValueError:
        raise InvalidAccessTokenException()

    repository = UserRepository(db)
    user = repository.get_by_id(user_id)

    if user is None:
        raise InvalidAccessTokenException()

    if not user.is_active:
        raise InactiveUserException()

    if payload.get("type") != "access":
        raise InvalidAccessTokenException()

    return user


def get_current_superuser(
        current_user: User = Depends(
            get_current_user,
        ),
) -> User:

    if not current_user.is_superuser:
        raise InsufficientPermissionsException()

    return current_user