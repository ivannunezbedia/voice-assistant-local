from __future__ import annotations

from abc import ABC, abstractmethod


class AudioInput(ABC):
    @abstractmethod
    def read(self) -> bytes:
        """Devuelve un bloque de audio capturado del micrófono."""


class AudioOutput(ABC):
    @abstractmethod
    def write(self, audio: bytes) -> None:
        """Emite audio al altavoz."""


class STTProvider(ABC):
    @abstractmethod
    def transcribe(self, audio: bytes) -> str:
        """Convierte audio en texto."""


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Genera texto de respuesta a partir del prompt."""


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """Devuelve audio sintetizado para el texto."""


class ProviderRegistry:
    """Registry simple para resolver proveedores por nombre."""

    def __init__(self) -> None:
        self._providers: dict[str, object] = {}

    def register(self, name: str, provider: object) -> None:
        self._providers[name] = provider

    def get(self, name: str) -> object:
        if name not in self._providers:
            raise KeyError(f"Proveedor no registrado: {name}")
        return self._providers[name]
