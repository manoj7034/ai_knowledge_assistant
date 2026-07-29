from fastapi import status
from app.exceptions.base import AppException


class InvalidCredentialsException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid email or password."


class InvalidTokenException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid authentication token."


class ExpiredTokenException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication token has expired."