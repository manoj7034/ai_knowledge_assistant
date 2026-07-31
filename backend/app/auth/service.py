from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.models.user import User
from app.auth.hashing import hash_password, verify_password
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import TokenResponse
from app.auth.token_service import TokenService
from app.exceptions.user import UserAlreadyExistsException
from app.exceptions.auth import InvalidCredentialsException


class AuthenticationService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(
    self,
    user_create: UserCreate,
    ) -> User:

        if self.user_repository.exists(user_create.email):
            raise UserAlreadyExistsException()

        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hash_password(user_create.password),
        )

        try:
            self.user_repository.save(user)
            # self.user_repository.db.commit()
            self.db.commit()
        except Exception:
            # self.user_repository.db.rollback()
            self.db.rollback()
            raise

        return user
    

    def login(
        self,
        credentials: UserLogin,
    ) -> TokenResponse:

        user = self.user_repository.get_by_email(
            credentials.email
        )

        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsException()

        # return TokenResponse(access_token=create_access_token(user.id),)
        token_service = TokenService(self.db)

        return token_service.create_token_pair(user)