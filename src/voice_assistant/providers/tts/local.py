from __future__ import annotations

from ..base import ProviderError
from ...interfaces import LLMProvider


class LocalLLMProvider(LLMProvider):
    """Implementación local mínima para generación de texto."""

    def generate(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise ProviderError("llm", "El prompt debe ser texto.")
        if not prompt.strip():
            raise ProviderError("llm", "El prompt no puede estar vacío.")
        return f"Respuesta local para: {prompt}"
