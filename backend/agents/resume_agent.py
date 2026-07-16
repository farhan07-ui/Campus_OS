import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# ----------------------------
# Load Environment Variables
# ----------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
You are CampusOS AI Resume Builder.

Your job is to interview the student one question at a time.

Collect:

• Full Name
• Email
• Phone
• LinkedIn
• Skills
• Education
• Projects
• Experience
• Certifications
• Achievements
• Career Objective

Only ask ONE question at a time.

Never generate the resume until requested.

Be professional and friendly.
"""
)


# ----------------------------
# Resume Session
# ----------------------------

class ResumeBuilderSession:

    def __init__(self):

        self.chat = model.start_chat(history=[])

        self.history = []

        response = self.chat.send_message(
            "Start the resume interview."
        )

        self.first_question = response.text

    def get_next_question(self, user_answer=None):

        if user_answer is None:
            return self.first_question

        self.history.append(user_answer)

        response = self.chat.send_message(user_answer)

        return response.text

    def generate_resume(self):

        transcript = "\n".join(self.history)

        prompt = f"""
Create a professional ATS-friendly resume
using the following information.

Return ONLY valid JSON.

Fields:

name

email

phone

linkedin

objective

education

skills

projects

experience

certifications

achievements

Transcript:

{transcript}
"""

        response = model.generate_content(prompt)

        return response.text


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    session = ResumeBuilderSession()

    print("\nCampusOS Resume Builder\n")

    print(session.get_next_question())

    while True:

        user = input("\nYou : ")

        if user.lower() == "done":
            break

        print("\nAI :", session.get_next_question(user))

    print("\nGenerating Resume...\n")

    resume = session.generate_resume()

    try:
        print(json.dumps(json.loads(resume), indent=4))
    except:
        print(resume)