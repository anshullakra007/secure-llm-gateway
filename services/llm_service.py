import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

async def generate_response(prompt: str) -> str:
    """
    Sends the sanitized prompt to the LLM and returns the response.
    """
    if not API_KEY:
        return "Warning: GEMINI_API_KEY not set. This is a mock response."
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}"
