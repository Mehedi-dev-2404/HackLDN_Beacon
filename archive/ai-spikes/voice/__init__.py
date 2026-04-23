"""
Aura Voice Module
ElevenLabs streaming integration
"""

from .eleven_stream import stream_text_to_speech, generate_audio_bytes

__all__ = [
    'stream_text_to_speech',
    'generate_audio_bytes'
]
