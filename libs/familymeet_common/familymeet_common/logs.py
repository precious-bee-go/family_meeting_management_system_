import json
import logging
import sys
from datetime import UTC, datetime
 
from .request_id import get_request_id
 
 
class JsonFormatter(logging.Formatter):
    """Write each log line as one JSON object, including the request id."""
 
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
 
    def format(self, record: logging.LogRecord) -> str:
        data = {
            "time": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "service": self.service_name,
            "request_id": get_request_id(),
            "message": record.getMessage(),
        }
        if record.exc_info:
            data["exception"] = self.formatException(record.exc_info)
        return json.dumps(data)
 
def setup_logging(service_name: str, level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter(service_name))
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
