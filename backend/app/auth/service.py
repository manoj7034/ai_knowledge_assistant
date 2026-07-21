from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.models.user import User
from app.auth.hashing import hash_password, verify_password
from app.schemas.user import UserCreate
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin
from app.auth.jwt import create_access_token


class AuthenticationService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(
        self,
        user_create: UserCreate,
    ) -> User:

        if self.user_repository.exists(user_create.email):
            raise ValueError("Email already exists")

        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            hashed_password=hash_password(user_create.password),
        )

        return self.user_repository.create(user)
    

    def login(
        self,
        credentials: UserLogin,
    ) -> Token:

        user = self.user_repository.get_by_email(
            credentials.email
        )

        if user is None:
            raise ValueError("Invalid credentials")

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid credentials")

        return Token(
            access_token=create_access_token(user.id)
        )