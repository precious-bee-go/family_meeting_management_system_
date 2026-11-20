from fastapi import FastAPI
 
from .errors import register_error_handlers
from .logs import setup_logging
from .request_id import RequestIdMiddleware
from .settings import ServiceSettings
 
 
def install_common(app: FastAPI, settings: ServiceSettings) -> None:
    """One call that gives a service logging, request ids and the standard error format."""
    setup_logging(settings.service_name, settings.log_level)
    app.add_middleware(RequestIdMiddleware)
    register_error_handlers(app)
