from fastapi import status

class AppException(Exception):
    def __init__(self, status_code: int, message: str, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(message)


class BadRequestException(AppException):
    def __init__(self, message: str = "Yêu cầu không hợp lệ", details=None):
        super().__init__(status.HTTP_400_BAD_REQUEST, message, details)


class ConflictException(AppException):
    def __init__(self, message: str = "Dữ liệu bị trùng", details=None):
        super().__init__(status.HTTP_409_CONFLICT, message, details)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Thông tin đăng nhập không hợp lệ", details=None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, details)


class TooManyRequestsException(AppException):
    def __init__(self, message: str = "Bạn đã thử quá nhiều lần", details=None):
        super().__init__(status.HTTP_429_TOO_MANY_REQUESTS, message, details)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Bạn không có quyền thực hiện thao tác này", details=None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, details)


class NotFoundException(AppException):
    def __init__(self, message: str = "Không tìm thấy tài nguyên", details=None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, details)
