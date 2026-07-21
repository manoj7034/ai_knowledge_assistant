from sqlalchemy.orm import Session

from app.repositories.user import UserRepository


class UserService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)