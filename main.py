from __future__ import annotations

from datetime import datetime, timezone

from .config import AppConfig
from .interfaces import AudioInput, AudioOutput, LLMProvider, STTProvider, TTSProvider
from .latency import LatencyLogger
from .models import PipelineMetrics, StageMetric
from .providers.base import ProviderError
from .state_machine import StateMachine


class VoicePipeline:
    """Orquesta el flujo micrófono -> STT -> LLM -> TTS -> altavoz."""

    def __init__(
        self,
        *,
        config: AppConfig | None = None,
        microphone: AudioInput | None = None,
        speaker: AudioOutput | None = None,
        stt: STTProvider | None = None,
        llm: LLMProvider | None = None,
        tts: TTSProvider | None = None,
        state_machine: StateMachine | None = None,
        latency_logger: LatencyLogger | None = None,
    ) -> None:
        self.config = config or AppConfig()
        self.microphone = microphone
        self.speaker = speaker
        self.stt = stt
        self.llm = llm
        self.tts = tts
        self.state_machine = state_machine or StateMachine()
        self.latency_logger = latency_logger or LatencyLogger()
        self.metrics = PipelineMetrics()

    def _record_stage(self, stage: str, action, *, error_message: str) -> object:
        started_at = datetime.now(timezone.utc)
        try:
            result = action()
            ended_at = datetime.now(timezone.utc)
            duration_ms = (ended_at - started_at).total_seconds() * 1000
            self.metrics.add(StageMetric(stage=stage, duration_ms=duration_ms, success=True, details=error_message))
            self.latency_logger.record(stage, started_at, ended_at, True, error_message)
            return result
        except Exception as exc:  # pragma: no cover - se captura por tests explícitos
            ended_at = datetime.now(timezone.utc)
            duration_ms = (ended_at - started_at).total_seconds() * 1000
            self.metrics.add(StageMetric(stage=stage, duration_ms=duration_ms, success=False, details=str(exc)))
            self.latency_logger.record(stage, started_at, ended_at, False, str(exc))
            raise ProviderError(stage, str(exc)) from exc

    def _ensure_dependencies(self) -> None:
        if self.microphone is None:
            raise ValueError("Se requiere un micrófono para ejecutar el pipeline.")
        if self.speaker is None:
            raise ValueError("Se requiere un altavoz para ejecutar el pipeline.")
        if self.stt is None:
            raise ValueError("Se requiere un proveedor STT.")
        if self.llm is None:
            raise ValueError("Se requiere un proveedor LLM.")
        if self.tts is None:
            raise ValueError("Se requiere un proveedor TTS.")

    def run_turn(self, audio: bytes | None = None) -> dict[str, object]:
        """Ejecuta un ciclo completo de voz con push-to-talk."""
        self._ensure_dependencies()
        self.state_machine.transition("LISTENING")

        try:
            captured_audio = audio if audio is not None else self.microphone.read()

            self.state_machine.transition("PROCESSING")
            transcript = self._record_stage(
                "stt",
                lambda: self.stt.transcribe(captured_audio),
                error_message="stt_failed",
            )

            response = self._record_stage(
                "llm",
                lambda: self.llm.generate(transcript),
                error_message="llm_failed",
            )

            synthesized_audio = self._record_stage(
                "tts",
                lambda: self.tts.synthesize(response),
                error_message="tts_failed",
            )

            self.state_machine.transition("SPEAKING")
            self.speaker.write(synthesized_audio)

            return {
                "transcript": transcript,
                "response": response,
                "audio": synthesized_audio,
                "latency": self.latency_logger.summary(),
                "metrics": self.metrics,
            }
        except Exception as exc:
            self.state_machine.transition("ERROR")
            raise RuntimeError(f"Fallo del pipeline de voz: {exc}") from exc
        finally:
            if self.state_machine.current.name in {"LISTENING", "PROCESSING", "SPEAKING", "ERROR"}:
                self.state_machine.transition("IDLE")


__all__ = ["VoicePipeline"]
