import os
import json
from typing import List, Optional
import google.generativeai as genai
from pydantic import BaseModel, Field

# 1. Configuration & API Key Setup
GOOGLE_API_KEY = "your-gemini-api-key-here"
genai.configure(api_key=GOOGLE_API_KEY)

# 2. Define the Resume Data Structure using Pydantic
class Education(BaseModel):
    institution: str
    degree: str
    graduation_year: str
    gpa_or_percentage: Optional[str] = None

class Experience(BaseModel):
    company: str
    role: str
    duration: str
    key_achievements: List[str] = Field(description="Bullet points of what you did")

class ResumeSchema(BaseModel):
    full_name: str
    email: str
    phone: str
    linkedin: Optional[str] = None
    skills: List[str]
    education: List[Education]
    experience: List[Experience]
    professional_summary: str = Field(description="A compelling 2-3 sentence career summary statement")

# 3. Conversational Pipeline Classes
class ResumeBuilderSession:
    def __init__(self):
        # Move instructions to system_instruction to prevent AI leakage on turn 1
        setup_prompt = """
        You are an expert Career Coach and Resume Interviewer for a University Placement Cell.
        Your goal is to gather information from the student one piece at a time to build a stellar resume.
        
        Follow this order carefully:
        1. Ask for their Full Name, Email, Phone Number, and LinkedIn Profile.
        2. Ask for their technical and soft skills.
        3. Ask about their educational background (College name, Degree, Year, GPA).
        4. Ask about any professional experience, internships, or major academic projects.
        
        Ask only ONE question at a time. Keep your tone encouraging and professional. 
        Do not output any JSON or final formatting yet. Just gather information sequentially.
        """
        
        # Fixed model name and set native behavior parameters
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=setup_prompt
        )
        
        self.chat = self.model.start_chat(history=[])
        self.collected_raw_text = []
        
        # Send an initial greeting to trigger the first structured question
        initial_response = self.chat.send_message("Hello! I am ready to start my resume interview.")
        self.first_message = initial_response.text
        self.collected_raw_text.append(f"AI: {self.first_message}")

    def get_next_question(self, user_input: str = None) -> str:
        """Sends the user's answer to the model and gets the next question."""
        if user_input is None:
            return self.first_message
        
        self.collected_raw_text.append(f"Student: {user_input}")
        response = self.chat.send_message(user_input)
        
        self.collected_raw_text.append(f"AI: {response.text}")
        return response.text

    def compile_final_resume(self) -> str:
        """
        Takes all the accumulated raw dialog text transcript 
        and outputs a perfectly formatted JSON structure matching ResumeSchema.
        """
        print("\n⚙️ Processing data and compiling structured resume...")
        
        full_transcript = "\n".join(self.collected_raw_text)
        compilation_prompt = f"""
        Analyze the following interview transcript and extract the details into the required structured schema. 
        Optimize bullet points and the professional summary to sound highly competitive for corporate placements.
        
        Transcript:
        {full_transcript}
        """
        
        response = self.model.generate_content(
            compilation_prompt,
            generation_config={
                "response_mime_type": "application/json", 
                "response_schema": ResumeSchema
            }
        )
        return response.text

# --- 🎯 Interactive Execution Example ---
if __name__ == "__main__":
    session = ResumeBuilderSession()
    
    print("--- 💼 Welcome to the Campus AI Resume Builder ---")
    print(f"\nAI: {session.get_next_question()}")
    
    turn_counter = 0
    max_turns = 4  # Adjusted for testing the foundational steps
    
    while turn_counter < max_turns:
        user_response = input("\nYou: ")
        if user_response.lower() in ['exit', 'quit', 'done']:
            break
            
        next_q = session.get_next_question(user_response)
        print(f"\nAI: {next_q}")
        turn_counter += 1
        
    print("\n--- 🏁 Interview Complete! Generating Draft ---")
    try:
        json_resume = session.compile_final_resume()
        
        parsed_resume = json.loads(json_resume)
        print(json.dumps(parsed_resume, indent=2))
        
        with open("student_resume.json", "w") as f:
            f.write(json_resume)
        print("\n✅ Clean resume data saved to 'student_resume.json'!")
    except Exception as e:
        print(f"❌ Extraction error: {e}")
