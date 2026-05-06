"""
Глобальные обработчики исключений и утилиты для FastAPI.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class APIException(Exception):
    """Базовое исключение для API с кодом статуса."""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(APIException):
    def __init__(self, resource: str, resource_id=None):
        message = f"{resource} не найден"
        if resource_id:
            message = f"{resource} с id={resource_id} не найден"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ValidationException(APIException):
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)


class ExternalServiceException(APIException):
    """Исключение при ошибке внешнего сервиса (Yandex Disk, News сайт)."""
    def __init__(self, service: str, message: str = None):
        msg = message or f"Ошибка подключения к {service}"
        super().__init__(msg, status.HTTP_503_SERVICE_UNAVAILABLE)


def setup_exception_handlers(app):
    """Настройка глобальных обработчиков исключений."""

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        logger.warning(f"APIException [{exc.status_code}]: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "details": exc.details,
                "status_code": exc.status_code
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        logger.warning(f"Validation error: {errors}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": True,
                "message": "Ошибка валидации данных",
                "details": {"validation_errors": errors},
                "status_code": 422
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Ошибка базы данных. Пожалуйста, попробуйте позже.",
                "status_code": 500
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Внутренняя ошибка сервера. Пожалуйста, попробуйте позже.",
                "status_code": 500
            }
        )
