import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------
# Placeholder Agent Functions
# Replace these with imports later
# ----------------------------

def syllabus_agent(query):
    return f"📚 Syllabus Agent\n\nReceived: {query}"


def assignment_agent(query):
    return f"📝 Assignment Agent\n\nReceived: {query}"


def timetable_agent(query):
    return f"📅 Timetable Agent\n\nReceived: {query}"


def resume_agent(query):
    return f"📄 Resume Agent\n\nReceived: {query}"


# ----------------------------
# Intent Classification
# ----------------------------

def classify_query(query: str):

    prompt = f"""
You are an AI Supervisor for CampusOS.

Determine which ONE agent should answer the user's query.

Available agents:

1. syllabus
- syllabus
- notes
- subject
- unit
- module
- pdf
- explain topic
- study material

2. assignment
- assignment
- homework
- summarize assignment
- explain assignment
- checklist

3. timetable
- timetable
- schedule
- study plan
- weekly routine
- daily routine

4. resume
- resume
- cv
- ats
- skills
- projects
- career

Return ONLY ONE WORD.

Possible outputs:

syllabus
assignment
timetable
resume

User Query:
{query}
"""

    response = model.generate_content(prompt)

    return response.text.strip().lower()


# ----------------------------
# Supervisor
# ----------------------------

def supervisor(query: str):

    agent = classify_query(query)

    print(f"\nSelected Agent: {agent}")

    if agent == "syllabus":
        return syllabus_agent(query)

    elif agent == "assignment":
        return assignment_agent(query)

    elif agent == "timetable":
        return timetable_agent(query)

    elif agent == "resume":
        return resume_agent(query)

    else:
        return "Sorry, I couldn't determine which agent should answer your request."


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    while True:

        user_query = input("\nAsk CampusOS: ")

        if user_query.lower() == "exit":
            break

        result = supervisor(user_query)

        print("\n" + result)