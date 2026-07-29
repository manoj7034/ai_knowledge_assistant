from fastapi import status


class AppException(Exception):
    # Base application exception.
    

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal Server Error"

    def __init__(
        self,
        detail: str | None = None,
    ):
        if detail is not None:
            self.detail = detail

        super().__init__(self.detail)