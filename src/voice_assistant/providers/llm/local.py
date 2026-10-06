from __future__ import annotations

from ..base import ProviderError
from ...interfaces import STTProvider


class LocalSTTProvider(STTProvider):
    """Implementación local mínima para transcripción."""

    def transcribe(self, audio: bytes) -> str:
        if not isinstance(audio, (bytes, bytearray)):
            raise ProviderError("stt", "El audio debe ser bytes.")
        payload = bytes(audio)
        if not payload:
            return "silencio"
        return "transcripción local generada"
