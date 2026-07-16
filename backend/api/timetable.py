from fastapi import APIRouter
from pydantic import BaseModel

from agents.timetable_agent import generate_campus_timetable

router = APIRouter(prefix="/timetable", tags=["Timetable"])


class TimetableInput(BaseModel):
    constraints: str


@router.post("/generate")
def generate(data: TimetableInput):

    result = generate_campus_timetable(data.constraints)

    return {
        "timetable": result
    }