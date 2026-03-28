class AppException(Exception):
    """Базовое исключение приложения"""

    message: str = "Internal server error"
    status_code: int = 500


class OrderAlreadyExistsError(AppException):
    message = "Order already exists"
    status_code = 409


class OrderNotFoundError(AppException):
    message = "Order not found"
    status_code = 404


class OrderCreationError(AppException):
    message = "Failed to create order"
    status_code = 500
