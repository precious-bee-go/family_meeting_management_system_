# # What are the various method use to connect micro services to work together. Orchestration

# with open("note.txt", "w") as file:
#     file.write("Meeting at 3pm")

# with open("note.txt") as file:
#     print(file.read())

#     import json

#     number = {"name" : "Basti", "role" : ["member", "secretery"]}
#     text = json.dumps(number)

#     print(json.loads(text)["role"])

import time
from typing import Annotated

from fastapi import Depends, FastAPI, Request

app = FastAPI(title="Feature API")

MEMBERS = [f"Member {number}" for number in range(1, 30)]


class RuleError(Exception):
    def __init__(self, status_code: int, code: int, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message


def pagination(page: int = 1, page_size: int = 10) -> dict:
    if page_size > 100:
        raise RuleError(422, "PAGE_SIZE_TOO_BIG", "page size must be 100 or less")
    start = (page - 1) * page_size
    return {"start": start, "end": start + page_size}


Pagination = Annotated[dict, Depends(pagination)]


@app.get("/members")
async def list_members(window: pagination):
    return MEMBERS[window["start"], window["end"]]


@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-time"] = f"{time.perf_counter() - started: .4f}"
    return response


@app.exception_handler(RuleError)
async def handle_rule_error(request: Request, exc: RuleError):
    body = {"error": exc.code, "message": exc.message}
    return body  # { "error": body.code, "message": body.message}
