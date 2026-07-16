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

model = genai.GenerativeModel("gemini-2.5-flash")


# ----------------------------
# Timetable Generator
# ----------------------------

def generate_timetable(user_input: str):

    prompt = f"""
You are CampusOS AI Timetable Generator.

Create a professional weekly timetable.

Instructions:

• Generate timetable from Monday to Friday.

• Distribute subjects evenly.

• Avoid scheduling conflicts.

• Add lunch break if appropriate.

• Return ONLY valid JSON.

JSON format:

{{
  "Monday":[
      {{
        "time":"",
        "subject":"",
        "room":""
      }}
  ],

  "Tuesday":[],

  "Wednesday":[],

  "Thursday":[],

  "Friday":[]

}}

User Requirements:

{user_input}

"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Error : {e}"


# ----------------------------
# Pretty JSON
# ----------------------------

def pretty_print(result):

    try:

        parsed = json.loads(result)

        return json.dumps(parsed, indent=4)

    except:

        return result


# ----------------------------
# Save JSON
# ----------------------------

def save_json(result, filename="generated_timetable.json"):

    try:

        with open(filename, "w", encoding="utf-8") as file:

            file.write(pretty_print(result))

        print(f"\n✅ Saved as {filename}")

    except Exception as e:

        print(e)


# ----------------------------
# Test
# ----------------------------

if __name__ == "__main__":

    print("\n===== CampusOS Timetable Generator =====\n")

    user_constraints = input("Enter timetable requirements:\n\n")

    print("\nGenerating timetable...\n")

    timetable = generate_timetable(user_constraints)

    formatted = pretty_print(timetable)

    print(formatted)

    save_json(timetable)