from fastapi import FastAPI

from api.assignment import router as assignment_router
from api.resume import router as resume_router
from api.timetable import router as timetable_router
from api.chat import router as chat_router

app = FastAPI(title="Campus OS")

app.include_router(chat_router)
app.include_router(assignment_router)
app.include_router(resume_router)
app.include_router(timetable_router)


@app.get("/")
def root():
    return {
        "message": "Campus OS Backend Running"
    }