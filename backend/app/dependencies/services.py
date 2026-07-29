from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.service import AuthenticationService
from app.dependencies.database import get_db


def get_authentication_service(db: Session = Depends(get_db),) -> AuthenticationService:
    return AuthenticationService(db)