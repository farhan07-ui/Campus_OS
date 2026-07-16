from fastapi import APIRouter
from pydantic import BaseModel

from agents.resume_agent import ResumeBuilderSession

router = APIRouter(prefix="/resume", tags=["Resume"])


class UserAnswer(BaseModel):
    message: str


session = ResumeBuilderSession()


@router.get("/start")
def start():

    return {
        "question": session.get_next_question()
    }


@router.post("/chat")
def chat(data: UserAnswer):

    question = session.get_next_question(data.message)

    return {
        "reply": question
    }


@router.get("/generate")
def generate():

    resume = session.compile_final_resume()

    return {
        "resume": resume
    }