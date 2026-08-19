from fastapi import status


class AppException(Exception):
    def __init__(self, status_code: int, message: str, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(message)


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", details=None):
        super().__init__(status.HTTP_400_BAD_REQUEST, message, details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden", details=None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, details)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details=None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, details)
