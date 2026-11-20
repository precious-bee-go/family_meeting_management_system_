import logging
from typing import Any
 
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException
 
from .request_id import get_request_id
 
logger = logging.getLogger("familymeet")
 
HTTP_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
}
 
 
class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[Any] = Field(default_factory=list)
    request_id: str | None = None
 
 
class ErrorResponse(BaseModel):
    error: ErrorBody
 
 
class AppError(Exception):
    """A business-rule error. Example: AppError(409, "DUPLICATE_VOTE", "Already voted.")"""
 
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: list[Any] | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or []
 
 
def _error_response(
    request: Request,
    status_code: int,
    code: str,
    message: str,
    details: list[Any] | None = None,
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", None) or get_request_id()
    body = ErrorResponse(
        error=ErrorBody(code=code, message=message, details=details or [], request_id=request_id)
    )
    return JSONResponse(status_code=status_code, content=body.model_dump())
 
 
def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        return _error_response(request, exc.status_code, exc.code, exc.message, exc.details)
 
    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        details = [
            {"field": ".".join(str(part) for part in err["loc"]), "message": err["msg"]}
            for err in exc.errors()
        ]
        return _error_response(
            request, 422, "VALIDATION_ERROR", "The request data is not valid.", details
        )
 
    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(request: Request, exc: StarletteHTTPException):
        code = HTTP_CODES.get(exc.status_code, "HTTP_ERROR")
        return _error_response(request, exc.status_code, code, str(exc.detail))
 
    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        logger.exception("Unhandled error")
        return _error_response(request, 500, "INTERNAL_ERROR", "Something went wrong on our side.")
