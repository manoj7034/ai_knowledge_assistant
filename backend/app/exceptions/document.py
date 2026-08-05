from fastapi import status
from app.exceptions.base import AppException


class DocumentNotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Document not found."


class InvalidDocumentException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid document."


class UnsupportedFileTypeException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Unsupported file type."


class FileTooLargeException(AppException):
    status_code = status.HTTP_413_CONTENT_TOO_LARGE
    detail = "File size exceeds the allowed limit."