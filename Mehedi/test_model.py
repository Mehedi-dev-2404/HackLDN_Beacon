import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "❌ API key not found!\n"
        "Please add GOOGLE_API_KEY to your .env file.\n"
        "Get a new key from: https://aistudio.google.com/app/apikey"
    )

print(f"✅ API key loaded: {api_key[:10]}...")

# Initialize client with new google-genai SDK
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",  # Updated model name
        contents="Say hello in one sentence."
    )
    
    print(f"✅ Success!\n\n{response.text}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    if "expired" in str(e).lower() or "invalid" in str(e).lower():
        print("\n🔑 Your API key is expired or invalid.")
        print("👉 Get a new key from: https://aistudio.google.com/app/apikey")
        print("👉 Then update your .env file with the new key")
    raise