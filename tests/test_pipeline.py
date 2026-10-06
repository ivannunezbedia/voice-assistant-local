import pytest
from voice_assistant.config import AppConfig
from voice_assistant.devices import Microphone, Speaker
from voice_assistant.pipeline import VoicePipeline
from voice_assistant.providers.base import ProviderError
from voice_assistant.providers.llm.local import LocalLLMProvider
from voice_assistant.providers.stt.local import LocalSTTProvider
from voice_assistant.providers.tts.local import LocalTTSProvider
from voice_assistant.state_machine import StateMachine


class TestVoicePipelineEndToEnd:
    """Pruebas del flujo completo del pipeline de voz."""

    def test_pipeline_runs_successfully(self) -> None:
        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=Microphone(audio=b"audio-test"),
            speaker=Speaker(),
            stt=LocalSTTProvider(),
            llm=LocalLLMProvider(),
            tts=LocalTTSProvider(),
        )

        result = pipeline.run_turn()

        assert result["transcript"] == "transcripción local generada"
        assert result["response"] == "Respuesta local para: transcripción local generada"
        assert result["audio"] == b"audio-local-tts"
        assert pipeline.state_machine.current.name == "IDLE"

    def test_pipeline_records_latency(self) -> None:
        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=Microphone(audio=b"audio-test"),
            speaker=Speaker(),
            stt=LocalSTTProvider(),
            llm=LocalLLMProvider(),
            tts=LocalTTSProvider(),
        )

        result = pipeline.run_turn()
        latency = result["latency"]

        assert "stt" in latency
        assert "llm" in latency
        assert "tts" in latency
        assert all(duration > 0 for duration in latency.values())

    def test_pipeline_handles_stt_failure(self) -> None:
        class FailingSTT(LocalSTTProvider):
            def transcribe(self, audio: bytes) -> str:
                raise ValueError("STT error")

        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=Microphone(audio=b"audio-test"),
            speaker=Speaker(),
            stt=FailingSTT(),
            llm=LocalLLMProvider(),
            tts=LocalTTSProvider(),
        )

        with pytest.raises(RuntimeError, match="Fallo del pipeline"):
            pipeline.run_turn()

        assert pipeline.state_machine.current.name == "IDLE"

    def test_pipeline_handles_llm_failure(self) -> None:
        class FailingLLM(LocalLLMProvider):
            def generate(self, prompt: str) -> str:
                raise ValueError("LLM error")

        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=Microphone(audio=b"audio-test"),
            speaker=Speaker(),
            stt=LocalSTTProvider(),
            llm=FailingLLM(),
            tts=LocalTTSProvider(),
        )

        with pytest.raises(RuntimeError, match="Fallo del pipeline"):
            pipeline.run_turn()

        assert pipeline.state_machine.current.name == "IDLE"

    def test_pipeline_handles_tts_failure(self) -> None:
        class FailingTTS(LocalTTSProvider):
            def synthesize(self, text: str) -> bytes:
                raise ValueError("TTS error")

        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=Microphone(audio=b"audio-test"),
            speaker=Speaker(),
            stt=LocalSTTProvider(),
            llm=LocalLLMProvider(),
            tts=FailingTTS(),
        )

        with pytest.raises(RuntimeError, match="Fallo del pipeline"):
            pipeline.run_turn()

        assert pipeline.state_machine.current.name == "IDLE"

    def test_pipeline_requires_all_dependencies(self) -> None:
        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=None,
            speaker=Speaker(),
            stt=LocalSTTProvider(),
            llm=LocalLLMProvider(),
            tts=LocalTTSProvider(),
        )

        with pytest.raises(ValueError, match="micrófono"):
            pipeline.run_turn()

    def test_pipeline_transitions_through_all_states(self) -> None:
        state_machine = StateMachine()
        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=Microphone(audio=b"audio-test"),
            speaker=Speaker(),
            stt=LocalSTTProvider(),
            llm=LocalLLMProvider(),
            tts=LocalTTSProvider(),
            state_machine=state_machine,
        )

        assert state_machine.current.name == "IDLE"
        result = pipeline.run_turn()
        assert state_machine.current.name == "IDLE"

    def test_pipeline_accepts_custom_audio(self) -> None:
        custom_audio = b"custom-audio-bytes"
        pipeline = VoicePipeline(
            config=AppConfig(),
            microphone=Microphone(audio=b"default-audio"),
            speaker=Speaker(),
            stt=LocalSTTProvider(),
            llm=LocalLLMProvider(),
            tts=LocalTTSProvider(),
        )

        result = pipeline.run_turn(audio=custom_audio)
        assert result["transcript"] == "transcripción local generada"
