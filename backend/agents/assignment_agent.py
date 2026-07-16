import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# ----------------------------
# Load Environment Variables
# ----------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------
# Assignment Solver
# ----------------------------

def solve_assignment(file_path: str, student_notes: str = "") -> str:
    """
    Reads an assignment (PDF or Image)
    and generates step-by-step educational solutions.
    """

    if not os.path.exists(file_path):
        return "❌ File not found."

    prompt = f"""
You are CampusOS AI Assignment Assistant.

Analyze the uploaded assignment carefully.

Instructions:

1. Identify every question.
2. Explain each solution step-by-step.
3. Never skip mathematical steps.
4. Use headings and bullet points.
5. If formulas are needed, explain them.
6. Keep explanations educational.
7. Do not simply provide final answers.

Student Notes:
{student_notes}
"""

    extension = os.path.splitext(file_path)[1].lower()

    try:

        if extension in [".png", ".jpg", ".jpeg", ".webp"]:

            image = Image.open(file_path)

            response = model.generate_content(
                [prompt, image]
            )

            return response.text

        elif extension == ".pdf":

            uploaded_file = genai.upload_file(path=file_path)

            response = model.generate_content(
                [prompt, uploaded_file]
            )

            genai.delete_file(uploaded_file.name)

            return response.text

        else:

            return "❌ Only PDF, PNG, JPG and JPEG files are supported."

    except Exception as e:

        return f"❌ Error: {e}"


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    file = input("Enter assignment file path: ")

    notes = input("Student Notes (optional): ")

    answer = solve_assignment(file, notes)

    print("\n")
    print(answer)