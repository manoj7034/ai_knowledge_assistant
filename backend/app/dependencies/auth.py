from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.exceptions.user import UserNotFoundException


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token)

    user_id = UUID(payload["sub"])

    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        raise UserNotFoundException()

    return user