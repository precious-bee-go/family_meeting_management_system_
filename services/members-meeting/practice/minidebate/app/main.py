from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.response import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Mini Debate API")

class RuleError(Exception):
    def __init__(self, status_code: int, code: int, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message

@app.exception_handler(RuleError)
async def handle_rule_error(request: Request, exc: RuleError):
    body = { "error" : { "code" : exc.code, "message" : exc.message}}
    return JSONResponse(status_code=exc.status_code, content=body)

class DebateCreate(BaseModel):
    title: str = Field(min_length=3)

class VoteCreate(BaseModel):
    member: str = Field(min_length=1)
    choice: str = Field(pattern="^(yes|no|abstain)$")

class Debate(BaseModel):
    id: int
    title: str
    status: str = "open"
    votes: dict[str, str] = {}

DEBATES: dict[int, Debate] = {}

def get_debate(debate_id: int) -> Debate:
    debate = DEBATES.get(debate_id)
    if debate is None:
        raise RuleError(404, "NOT_FOUND", "Debate not Found")

DebateDep = Annotated[Debate, Depends(get_debate)]

@app.post("/debates", status_code=201)
def create_debate(data: DebateCreate) -> Debate:
    debate = Debate(id=len(DEBATES) + 1, title=data.title)
    DEBATES[debate.id] = debate
    return debate

