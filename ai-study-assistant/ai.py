import os
from google import genai
from dotenv import load_dotenv

# Load the API key from your .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key not found or expired! Please add your new key to the .env file.")

# Initialize the client
client = genai.Client(api_key=api_key)

def generate_summary(text):
    prompt = f"""
    You are an AI Study Assistant. Read the following text and provide:
    1. A short summary (5-6 lines).
    2. A detailed summary using bullet points.
    3. A list of key concepts.
    Keep the language simple for a student.
    
    Text: {text}
    """
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    return response.text

def generate_quiz(text):
    prompt = f"""
    You are an AI Study Assistant. Generate a study test based on the following text.
    Include 5 Multiple Choice Questions, 3 Short Answer Questions, and 2 True/False Questions.
    Provide the answers clearly at the very bottom.
    
    Text: {text}
    """
    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    return response.text