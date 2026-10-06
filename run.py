#!/usr/bin/env python3
"""Script de entrada para ejecutar el asistente de voz local."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from voice_assistant.config import AppConfig
from voice_assistant.devices import Microphone, Speaker
from voice_assistant.pipeline import VoicePipeline
from voice_assistant.providers.llm.local import LocalLLMProvider
from voice_assistant.providers.stt.local import LocalSTTProvider
from voice_assistant.providers.tts.local import LocalTTSProvider


def main() -> None:
    print("\n=== Asistente de Voz Local ===")
    print("Inicializando pipeline...\n")

    config = AppConfig()

    pipeline = VoicePipeline(
        config=config,
        microphone=Microphone(audio=b"audio-simulacion"),
        speaker=Speaker(),
        stt=LocalSTTProvider(),
        llm=LocalLLMProvider(),
        tts=LocalTTSProvider(),
    )

    print("Pipeline creado correctamente.")
    print(f"Config: STT={config.stt_provider}, LLM={config.llm_provider}, TTS={config.tts_provider}")
    print("\nEjecutando ciclo de voz...\n")

    result = pipeline.run_turn()

    print(f"✓ Transcript: {result['transcript']}")
    print(f"✓ Response: {result['response']}")
    print(f"✓ Audio size: {len(result['audio'])} bytes")
    print(f"\nLatency (ms):")
    for stage, duration in result["latency"].items():
        print(f"  - {stage}: {duration:.2f}ms")
    print(f"\n✓ Estado final: {pipeline.state_machine.current.name}")
    print("\n=== Ciclo completado ===")


if __name__ == "__main__":
    main()
