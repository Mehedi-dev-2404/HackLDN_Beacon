from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.utils.time import utc_now_iso


logger = get_logger(__name__)


class AppError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        code: str = "APP_ERROR",
        details: object | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details


class StartupError(AppError):
    def __init__(self, message: str, details: object | None = None) -> None:
        super().__init__(
            message=message,
            status_code=500,
            code="STARTUP_ERROR",
            details=details,
        )


def _error_payload(
    request: Request,
    message: str,
    code: str,
    details: object | None = None,
) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "path": request.url.path,
            "timestamp": utc_now_iso(),
        }
    }


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(
            request=request,
            message=exc.message,
            code=exc.code,
            details=exc.details,
        ),
    )


async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=_error_payload(
            request=request,
            message="Validation failed",
            code="VALIDATION_ERROR",
            details=exc.errors(),
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    details = exc.detail if isinstance(exc.detail, (dict, list)) else {"detail": exc.detail}
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(
            request=request,
            message="HTTP error",
            code="HTTP_ERROR",
            details=details,
        ),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=500,
        content=_error_payload(
            request=request,
            message="Internal server error",
            code="INTERNAL_ERROR",
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
