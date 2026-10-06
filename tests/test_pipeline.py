from __future__ import annotations

from voice_assistant.config import AppConfig
from voice_assistant.devices import Microphone, Speaker
from voice_assistant.pipeline import VoicePipeline
from voice_assistant.providers.llm.local import LocalLLMProvider
from voice_assistant.providers.stt.local import LocalSTTProvider
from voice_assistant.providers.tts.local import LocalTTSProvider


def main() -> None:
    config = AppConfig()
    pipeline = VoicePipeline(
        config=config,
        microphone=Microphone(audio=b"audio-simulacion"),
        speaker=Speaker(),
        stt=LocalSTTProvider(),
        llm=LocalLLMProvider(),
        tts=LocalTTSProvider(),
    )

    result = pipeline.run_turn()
    print("transcript:", result["transcript"])
    print("response:", result["response"])
    print("latency:", result["latency"])
    print("speaker_buffer_size:", len(result["audio"]))


if __name__ == "__main__":
    main()


__all__ = ["main"]
