import base64
from collections.abc import Iterable


class ElevenLabsVoiceService:
    def __init__(self, api_key: str = "") -> None:
        self.api_key = api_key.strip()

    def _load_client(self):
        if not self.api_key:
            raise RuntimeError("ELEVEN_LABS_API_KEY is not configured")
        try:
            from elevenlabs import generate, set_api_key
        except Exception as exc:
            raise RuntimeError("elevenlabs package is not installed") from exc
        set_api_key(self.api_key)
        return generate

    def _to_bytes(self, audio: object) -> bytes:
        if isinstance(audio, (bytes, bytearray)):
            return bytes(audio)
        if isinstance(audio, Iterable):
            chunks = [chunk for chunk in audio if isinstance(chunk, (bytes, bytearray))]
            return b"".join(chunks)
        raise RuntimeError("Unexpected audio payload from ElevenLabs")

    def synthesize_base64(
        self,
        text: str,
        voice: str = "Rachel",
        model: str = "eleven_monolingual_v1",
    ) -> dict:
        generate = self._load_client()
        audio = generate(text=text, voice=voice, model=model, stream=False)
        audio_bytes = self._to_bytes(audio)
        return {
            "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
            "content_type": "audio/mpeg",
            "voice": voice,
            "model": model,
        }
