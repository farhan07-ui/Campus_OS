import os
import json
from typing import List
import google.generativeai as genai
from pydantic import BaseModel, Field

# 1. Configuration & API Key Setup
GOOGLE_API_KEY = "your-gemini-api-key-here"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. Define the exact database/UI schema using Pydantic
class TimeSlot(BaseModel):
    time: str = Field(description="The time interval, e.g., '09:00 AM - 10:00 AM'")
    subject: str = Field(description="Name of the subject allocated, or 'Break / Free Period'")
    room: str = Field(description="Assigned classroom or lab space, if applicable")

class DaySchedule(BaseModel):
    day: str = Field(description="Day of the week, e.g., 'Monday'")
    slots: List[TimeSlot]

class CompleteTimetable(BaseModel):
    timetable: List[DaySchedule]
    notes: str = Field(description="Any specific conflict resolutions or scheduling logic applied by the AI")

def generate_campus_timetable(input_constraints: str) -> str:
    """
    Leverages Gemini's structured JSON output to create a collision-free 
    timetable based on input data text constraints.
    """
    # Initialize the model
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    system_prompt = """
    You are an expert University Academic Registrar and scheduling algorithm. 
    Your job is to generate a comprehensive, conflict-free weekly class timetable (Monday to Friday) 
    based on the subjects, credit hours, and time parameters provided by the user.

    Scheduling Rules:
    1. Distribute the required hours evenly across the week.
    2. Do not exceed the total available hours per day.
    3. Ensure logical placement for lunch breaks or recess periods if appropriate.
    4. If the constraints are impossible to fulfill perfectly, approximate the best solution and explain why in the notes field.
    """

    # Call the model forcing a JSON response that fits our Pydantic classes exactly
    response = model.generate_content(
        f"{system_prompt}\n\nUser Constraints:\n{input_constraints}",
        generation_config={"response_mime_type": "application/json", "response_schema": CompleteTimetable}
    )

    return response.text

# --- 🎯 Execution Example ---
if __name__ == "__main__":
    # Simulated input a student or department head might type or upload
    raw_user_input = """
    Subjects to schedule:
    - Advanced Machine Learning: 4 hours required per week.
    - Distributed Systems: 3 hours required per week.
    - Cloud Computing Lab: 2 hours required per week (must be a single contiguous 2-hour block).
    - Technical Communication: 2 hours required per week.

    Daily Availability:
    - Monday through Friday.
    - Classes can only run between 09:00 AM and 01:00 PM.
    - Include a 30-minute recess or free slot every day around 11:00 AM if possible.
    """

    print("🔄 Generating optimized timetable grid...")
    json_timetable_output = generate_campus_timetable(raw_user_input)
    
    # Pretty print the resulting JSON
    parsed_json = json.loads(json_timetable_output)
    print(json.dumps(parsed_json, indent=2))
    
    # Save it out as a file that can be read by a web frontend interface
    with open("generated_timetable.json", "w") as f:
        f.write(json_timetable_output)
    print("\n✅ Timetable JSON exported successfully to 'generated_timetable.json'")
