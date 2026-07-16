import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# ----------------------------
# Load Environment Variables
# ----------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------
# Read PDF
# ----------------------------

def read_syllabus(pdf_path: str):

    if not os.path.exists(pdf_path):
        return None

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ----------------------------
# Ask Questions
# ----------------------------

def query_syllabus(pdf_path: str, question: str):

    syllabus_text = read_syllabus(pdf_path)

    if syllabus_text is None:
        return "❌ Syllabus PDF not found."

    prompt = f"""
You are CampusOS AI Syllabus Assistant.

You must answer ONLY from the syllabus provided below.

Rules:

1. Never invent information.

2. If the answer is not present,
reply:

"I couldn't find that information in the syllabus."

3. Explain clearly.

4. Use headings and bullet points whenever needed.

------------------------

SYLLABUS

{syllabus_text}

------------------------

Student Question:

{question}

"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error : {e}"


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    pdf = input("Enter syllabus PDF path: ")

    while True:

        question = input("\nAsk Question (type exit): ")

        if question.lower() == "exit":
            break

        answer = query_syllabus(pdf, question)

        print("\n")
        print(answer)