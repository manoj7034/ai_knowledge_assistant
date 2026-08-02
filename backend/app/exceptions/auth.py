from fastapi import status
from app.exceptions.base import AppException


class InvalidCredentialsException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid email or password."


class InvalidAccessTokenException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid access token."


class ExpiredAccessTokenException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Access token has expired."


class InvalidRefreshTokenException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid refresh token."


class RefreshTokenExpiredException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Refresh token has expired."