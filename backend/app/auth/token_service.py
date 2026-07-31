import secrets
import hashlib
from sqlalchemy.orm import Session
from datetime import UTC, datetime, timedelta

from app.repositories.refresh_token import RefreshTokenRepository
from app.auth.jwt import create_access_token
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.token import TokenResponse
from app.config.settings import settings


class TokenService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.refresh_token_repository = (
            RefreshTokenRepository(db)
        )

    @staticmethod
    def generate_refresh_token() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def hash_refresh_token(refresh_token: str, ) -> str:
        return hashlib.sha256(refresh_token.encode()).hexdigest()

    def create_token_pair(self, user: User,) -> TokenResponse:
        access_token = create_access_token(user.id,)
        refresh_token = self.generate_refresh_token()
        token_hash = self.hash_refresh_token(refresh_token,)

        refresh_token_model = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=(datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)),
            )

        try:
            self.refresh_token_repository.save(refresh_token_model,)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return TokenResponse(
            access_token=access_token, 
            refresh_token=refresh_token,
            token_type="bearer",
            )
    