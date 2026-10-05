from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AppConfig:
    """Configuración central del sistema de voz."""

    stt_provider: str = "local"
    llm_provider: str = "local"
    tts_provider: str = "local"
    push_to_talk: bool = True
    log_latencies: bool = True
    timeout_seconds: float = 30.0
    sample_rate_hz: int = 16000
    channel_count: int = 1
    model_name: str = "default-model"
    output_format: str = "wav"
    enable_cloud_fallback: bool = False
    fallback_provider: Optional[str] = None

    @property
    def stage_names(self) -> list[str]:
        return ["stt", "llm", "tts"]
