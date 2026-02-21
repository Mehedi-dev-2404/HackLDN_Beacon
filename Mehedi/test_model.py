import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Validate key exists
if not api_key:
    raise ValueError(
        "Missing GOOGLE_API_KEY in .env file.\n"
        "Please create a .env file with:\n"
        "GOOGLE_API_KEY=your_actual_api_key_here"
    )

# Verify key format (should start with AIza)
if not api_key.startswith("AIza"):
    print(f"⚠️  Warning: API key doesn't start with 'AIza' - might be invalid")
    print(f"Key preview: {api_key[:10]}...")

print(f"✅ API key loaded: {api_key[:10]}...")

# Initialize client with new google-genai SDK
client = genai.Client(api_key=api_key)

try:
    # Generate content using the new SDK syntax
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",  # Use available model
        contents="Explain recursion like I'm 5."
    )
    
    print("\n📝 Response:")
    print(response.text)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Verify your API key is valid in Google AI Studio")
    print("2. Check if Generative Language API is enabled")
    print("3. Try generating a new API key")
    print("4. Ensure you're using the correct project")