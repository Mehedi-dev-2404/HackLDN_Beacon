import os
import sys
from elevenlabs import generate, stream, set_api_key
from typing import Iterator

# Add backend directory to path for config imports
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from config import ELEVEN_KEY

# Set API key globally (do not reinitialize in routes)
set_api_key(ELEVEN_KEY)


def stream_text_to_speech(
    text: str,
    voice: str = "Rachel",
    model: str = "eleven_monolingual_v1"
) -> Iterator[bytes]:
    """
    Stream text-to-speech using ElevenLabs API.
    
    Args:
        text: Text to convert to speech
        voice: ElevenLabs voice ID or name (default: Rachel - British accent)
        model: ElevenLabs model to use
        
    Returns:
        Iterator yielding audio chunks
        
    Raises:
        Exception: If streaming fails
    """
    try:
        audio_stream = generate(
            text=text,
            voice=voice,
            model=model,
            stream=True
        )
        
        return audio_stream
    
    except Exception as e:
        raise Exception(f"ElevenLabs streaming error: {str(e)}")


def generate_audio_bytes(
    text: str,
    voice: str = "Rachel",
    model: str = "eleven_monolingual_v1"
) -> bytes:
    """
    Generate complete audio bytes (non-streaming).
    
    Args:
        text: Text to convert to speech
        voice: ElevenLabs voice ID or name
        model: ElevenLabs model to use
        
    Returns:
        Complete audio as bytes
    """
    try:
        audio = generate(
            text=text,
            voice=voice,
            model=model,
            stream=False
        )
        
        return audio
    
    except Exception as e:
        raise Exception(f"ElevenLabs generation error: {str(e)}")
