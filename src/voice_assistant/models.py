from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AudioChunk:
    """Bloque de audio capturado por el micrófono."""

    data: bytes
    sample_rate: int = 16000
    channels: int = 1
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class StageMetric:
    """Métrica registrada para una etapa del flujo."""

    stage: str
    duration_ms: float
    success: bool
    details: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class PipelineMetrics:
    """Resumen del flujo completo."""

    stages: list[StageMetric] = field(default_factory=list)
    total_duration_ms: float = 0.0

    def add(self, stage: StageMetric) -> None:
        self.stages.append(stage)
        self.total_duration_ms = sum(item.duration_ms for item in self.stages)


@dataclass
class Transcription:
    text: str
    confidence: float = 1.0
    provider: str = "unknown"


@dataclass
class LLMResponse:
    text: str
    provider: str = "unknown"


@dataclass
class SynthesizedAudio:
    data: bytes
    provider: str = "unknown"


@dataclass
class VoiceEvent:
    name: str
    payload: dict[str, Any] | None = None
