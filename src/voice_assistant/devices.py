from __future__ import annotations

from .interfaces import AudioInput, AudioOutput


class Microphone(AudioInput):
    """Fuente de entrada de audio simple para pruebas o ejecución local."""

    def __init__(self, audio: bytes = b"") -> None:
        self._audio = audio

    def read(self) -> bytes:
        return self._audio


class Speaker(AudioOutput):
    """Receptor de salida de audio en memoria para pruebas o CLI local."""

    def __init__(self) -> None:
        self._buffer = bytearray()

    def write(self, audio: bytes) -> None:
        self._buffer.extend(audio)

    @property
    def buffer(self) -> bytes:
        return bytes(self._buffer)


class AudioFileInput(Microphone):
    """Alias útil para futuras integraciones con archivos de audio."""

    pass


class AudioFileOutput(Speaker):
    """Alias útil para futuras integraciones de salida a archivos."""

    pass
