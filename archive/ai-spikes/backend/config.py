import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

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

# Strip quotes if present (common .env issue)
if GEMINI_KEY:
    GEMINI_KEY = GEMINI_KEY.strip('"').strip("'")
if ELEVEN_KEY:
    ELEVEN_KEY = ELEVEN_KEY.strip('"').strip("'")

# Validate keys early (fail fast)
if not GEMINI_KEY:
    raise ValueError(
        "Missing GEMINI_API_KEY or GOOGLE_API_KEY in .env file\n"
        "Get a new key from: https://aistudio.google.com/app/apikey"
    )

if not ELEVEN_KEY:
    raise ValueError("Missing ELEVEN_LABS_API_KEY in .env file")

# Initialize Gemini client using new google-genai SDK
gemini_client = genai.Client(api_key=GEMINI_KEY)

# Default model to use
DEFAULT_MODEL = "gemini-2.5-flash"


def generate_content(prompt: str, temperature: float = 0.4, top_p: float = 0.8, top_k: int = 40) -> str:
    """
    Generate content using Gemini model.
    
    Args:
        prompt: The prompt to send to the model
        temperature: Sampling temperature (0.0-1.0)
        top_p: Nucleus sampling parameter
        top_k: Top-k sampling parameter
        
    Returns:
        Generated text response
    """
    response = gemini_client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
        config={
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
        }
    )
    return response.text