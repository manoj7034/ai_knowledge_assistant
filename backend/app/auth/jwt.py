from datetime import datetime, timedelta, UTC
from uuid import UUID
from jose import jwt, JWTError

from app.config.settings import settings


def create_access_token(user_id: UUID,) -> str:
    # Create a JWT access token

    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    # Decode and validate an access token

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )