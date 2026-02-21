import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Fetch API keys
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
ELEVEN_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# Validate keys early (fail fast)
if not GEMINI_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

if not ELEVEN_KEY:
    raise ValueError("Missing ELEVEN_LABS_API_KEY in .env file")

# Configure Gemini with API key
genai.configure(api_key=GEMINI_KEY)

# Expose reusable Gemini model instance
gemini_model = genai.GenerativeModel("models/gemini-1.5-pro-latest")