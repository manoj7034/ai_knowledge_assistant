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
from app.repositories.user import UserRepository
from app.exceptions.auth import InvalidRefreshTokenException, RefreshTokenExpiredException


class TokenService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.user_repository = UserRepository(db)
        self.refresh_token_repository = (
            RefreshTokenRepository(db)
        )        

    @staticmethod
    def generate_refresh_token() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def hash_refresh_token(refresh_token: str, ) -> str:
        return hashlib.sha256(refresh_token.encode()).hexdigest()

    def refresh_token(self, plain_refresh_token: str) -> TokenResponse:
            token_hash = self.hash_refresh_token(plain_refresh_token)
            stored_token = (self.refresh_token_repository
                            .get_active_by_hash(token_hash))

            if stored_token is None:
                 raise InvalidRefreshTokenException()

            if stored_token.expires_at < datetime.now(UTC):
                raise RefreshTokenExpiredException()

            user = self.user_repository.get_by_id(stored_token.user_id)
            
            if user is None:
                raise InvalidRefreshTokenException()

            try:
                self.refresh_token_repository.revoke(stored_token)

                response = self.create_token_pair(user, commit=False,)

                self.db.commit()

                return response

            except Exception:
                self.db.rollback()
                raise


    def create_token_pair(self, user: User, *, commit: bool = True) -> TokenResponse:
        access_token = create_access_token(user.id,)
        refresh_token = self.generate_refresh_token()
        token_hash = self.hash_refresh_token(refresh_token,)    

        refresh_token_entity  = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=(datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)),
            )

        try:
            self.refresh_token_repository.save(refresh_token_entity,)
            if commit:
               self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return TokenResponse(
            access_token=access_token, 
            refresh_token=refresh_token,
            token_type="bearer",
            )

    def logout(self, refresh_token: str) -> None:
        token_hash = self.hash_refresh_token(refresh_token)
        stored_token = self.refresh_token_repository.get_active_by_hash(token_hash)
        if stored_token is None:
            raise InvalidRefreshTokenException()

        self.refresh_token_repository.revoke(stored_token)

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
