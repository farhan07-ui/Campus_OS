from fastapi import APIRouter
from pydantic import BaseModel

from agents.supervisor import supervisor

router = APIRouter(prefix="/chat", tags=["Campus AI"])


class ChatRequest(BaseModel):
    query: str


@router.post("/")
def chat(data: ChatRequest):

    answer = supervisor(data.query)

    return {
        "response": answer
    }