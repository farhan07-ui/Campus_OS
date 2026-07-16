import os
from dotenv import load_dotenv
import google.generativeai as genai

from agents.resume_agent import ResumeBuilderSession
from agents.timetable_agent import generate_timetable

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------
# Resume Session
# ----------------------------

resume_session = ResumeBuilderSession()


# ----------------------------
# Intent Classification
# ----------------------------

def classify_query(query: str):

    prompt = f"""
You are the AI Supervisor of CampusOS.

Determine which ONE agent should handle the user's request.

Available agents:

1. syllabus
- syllabus
- notes
- subject
- unit
- module
- pdf
- study material

2. assignment
- assignment
- homework
- solve assignment
- explain assignment

3. timetable
- timetable
- schedule
- routine
- weekly plan
- study plan

4. resume
- resume
- cv
- ats
- placement
- projects
- skills
- interview

Return ONLY one word.

Possible outputs:

syllabus
assignment
timetable
resume

User Query:

""" + query

    response = model.generate_content(prompt)

    return response.text.strip().lower()


# ----------------------------
# Supervisor
# ----------------------------

def supervisor(query: str):

    agent = classify_query(query)

    print(f"\nSelected Agent : {agent}")

    if agent == "resume":

        return resume_session.get_next_question(query)

    elif agent == "timetable":

        return generate_timetable(query)

    elif agent == "assignment":

        return (
            "📄 Assignment Agent\n\n"
            "Please upload your assignment PDF or image "
            "using the Assignment module."
        )

    elif agent == "syllabus":

        return (
            "📚 Syllabus Agent\n\n"
            "Please upload your syllabus PDF "
            "using the Syllabus module."
        )

    return "Sorry, I couldn't understand your request."


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    print("\n===== CampusOS Supervisor =====\n")

    while True:

        query = input("You : ")

        if query.lower() == "exit":
            break

        answer = supervisor(query)

        print("\nCampusOS:\n")

        print(answer)