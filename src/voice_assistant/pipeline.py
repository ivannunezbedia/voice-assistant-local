from __future__ import annotations

from ..base import ProviderError
from ...interfaces import TTSProvider


class LocalTTSProvider(TTSProvider):
    """Implementación local mínima para síntesis de voz."""

    def synthesize(self, text: str) -> bytes:
        if not isinstance(text, str):
            raise ProviderError("tts", "El texto debe ser str.")
        if not text.strip():
            raise ProviderError("tts", "El texto no puede estar vacío.")
        return b"audio-local-tts"
