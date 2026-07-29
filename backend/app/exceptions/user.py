from fastapi import status
from app.exceptions.base import AppException


class UserAlreadyExistsException(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User with this email already exists."


class UserNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found."


class InactiveUserException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "User account is inactive."