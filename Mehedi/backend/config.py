import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from multiple possible locations
# Try: 1) backend/.env, 2) parent directory (Mehedi/.env), 3) system env
backend_env = Path(__file__).parent / ".env"
parent_env = Path(__file__).parent.parent / ".env"

if backend_env.exists():
    load_dotenv(backend_env)
elif parent_env.exists():
    load_dotenv(parent_env)
else:
    load_dotenv()  # Try default locations

# Fetch API keys
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
ELEVEN_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# Validate keys early (fail fast)
if not GEMINI_KEY:
    raise ValueError(
        "Missing GEMINI_API_KEY or GOOGLE_API_KEY in .env file\n"
        "Get a new key from: https://aistudio.google.com/app/apikey"
    )

if not ELEVEN_KEY:
    raise ValueError("Missing ELEVEN_LABS_API_KEY in .env file")

# Configure Gemini with API key
genai.configure(api_key=GEMINI_KEY)

# Expose reusable Gemini model instance
gemini_model = genai.GenerativeModel("models/gemini-1.5-pro-latest")