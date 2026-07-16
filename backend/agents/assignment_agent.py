import os
import google.generativeai as genai
from PIL import Image

# 1. Configuration & API Key Setup
# Replace with your actual Gemini API key or set the GEMINI_API_KEY environment variable
GOOGLE_API_KEY = "your-gemini-api-key-here"
genai.configure(api_key=GOOGLE_API_KEY)

def solve_assignment(file_path: str, student_notes: str = "") -> str:
    """
    Takes an assignment file (image or PDF), reads the questions, 
    and generates a step-by-step educational solution guide.
    """
    if not os.path.exists(file_path):
        return f"❌ Error: File not found at {file_path}"

    print(f"🔄 Analyzing assignment file: {file_path}...")

    # Initialize a multimodal model (Gemini 2.5 Flash is fast and excellent at multimodal tasks)
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    # Define strict pedagogical guardrails for the AI Teacher role
    prompt = """
    You are an expert AI Teacher and Academic Assistant for a University Operating System.
    Your task is to analyze the uploaded assignment image/document and solve the questions found within it.

    Please adhere to the following strict guidelines:
    1. Identify and list each question clearly.
    2. Provide a step-by-step breakdown explaining *how* to solve the problem, rather than just flashing the final answer.
    3. Use clear formatting (Markdown tables, bullet points, or structured headings) to separate different problems.
    4. If the question involves complex calculations, show the formulas used.
    5. If any additional context or hints are provided by the student, take them into account.
    """

    if student_notes:
        prompt += f"\n\nAdditional Student Notes/Context:\n{student_notes}"

    # Determine file type and process accordingly
    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        if file_extension in ['.png', '.jpg', '.jpeg', '.webp']:
            # Open the image file using Pillow
            image_data = Image.open(file_path)
            
            # Pass both the image object and the text prompt to the model
            response = model.generate_content([prompt, image_data])
            
        elif file_extension == '.pdf':
            # Upload the PDF file directly to Google's File API for processing
            pdf_file = genai.upload_file(path=file_path)
            
            # Pass the uploaded file reference and the text prompt
            response = model.generate_content([prompt, pdf_file])
            
            # Clean up the file from the cloud storage after processing
            genai.delete_file(pdf_file.name)
            
        else:
            return "❌ Unsupported file format. Please upload a PDF or an Image (PNG/JPEG)."

        return response.text

    except Exception as e:
        return f"❌ An error occurred during processing: {str(e)}"

# --- 🎯 Execution Example ---
if __name__ == "__main__":
    # Example 1: Solving a math/physics problem from a photo taken by a student
    # Make sure you have a real file named "calculus_hw.png" or adjust the path below
    sample_assignment = "calculus_hw.png"
    
    # Optional context the student can type into the app frontend
    extra_context = "This is for Physics 101. We are supposed to use the work-energy theorem."

    if os.path.exists(sample_assignment):
        solutions = solve_assignment(sample_assignment, student_notes=extra_context)
        
        print("\n--- 📚 Generated Solutions & Explanations ---")
        print(solutions)
        
        # Save the solution to a file so the student can read it later
        with open("assignment_solutions.md", "w", encoding="utf-8") as f:
            f.write(solutions)
        print("\n✅ Solutions saved to 'assignment_solutions.md'")
    else:
        print(f"Please place a valid file named '{sample_assignment}' in this directory to test.")
