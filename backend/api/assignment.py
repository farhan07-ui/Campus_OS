from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

from agents.assignment_agent import solve_assignment

router = APIRouter(prefix="/assignment", tags=["Assignment"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/solve")
async def solve(
    file: UploadFile = File(...),
    notes: str = Form("")
):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = solve_assignment(filepath, notes)

    return {
        "status": "success",
        "result": result
    }