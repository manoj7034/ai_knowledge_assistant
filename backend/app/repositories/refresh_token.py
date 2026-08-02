from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, db: Session,):
        super().__init__(db, RefreshToken)

    def get_by_hash( self, token_hash: str,) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        return self.db.scalar(stmt)

    def get_active_by_hash(self, token_hash: str,) -> RefreshToken | None:
        stmt = (
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None)
            )
        )

        return self.db.scalar(stmt)


    def revoke(self, refresh_token: RefreshToken,) -> None:
        refresh_token.revoked_at = datetime.now(UTC)
        self.db.flush()

    def revoke_all_for_user(self, user_id: UUID,) -> None:
        stmt = (update(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
        ).values(
            revoked_at = datetime.now(UTC),
        ))

        self.db.execute(stmt)

    def delete_expired(self, ) -> int:
        stmt = (
            delete(RefreshToken)
            .where(
                RefreshToken.expires_at < datetime.now(UTC),
            )
        )

        result = self.db.execute(stmt)

        return result.rowcount or 0 # type: ignore