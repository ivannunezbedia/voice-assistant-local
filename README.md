# Voice Assistant Local

Arquitectura propuesta para un asistente de voz modular, local-first y con push-to-talk.

## Objetivo

Construir un flujo de audio simple y extensible:

microfono -> STT -> LLM -> TTS -> altavoz

Cada proveedor queda detrás de una interfaz y puede ser local o remoto sin cambiar la lógica principal del sistema.

## Principios

- Local-first por defecto
- Cambio de proveedores sin reescrituras del flujo
- Registro y latencia por etapa
- Manejo de errores explícito
- Máquina de estados simple, sin UI ni memoria
- Sin agentes, sin memoria persistente, sin features adicionales

## Arquitectura general

- `devices`: entrada/salida de audio (micrófono y altavoz)
- `providers`: adaptadores para STT, LLM y TTS con implementaciones local/cloud
- `pipeline`: orquestación del flujo principal
- `state_machine`: estados y transiciones
- `latency`: logs de tiempos por etapa
- `tests`: validación por capas

## Árbol de archivos

```text
voice-assistant-local/
├── README.md
├── pyproject.toml
├── .gitignore
├── src/
│   └── voice_assistant/
│       ├── __init__.py
│       ├── config.py
│       ├── models.py
│       ├── interfaces.py
│       ├── latency.py
│       ├── state_machine.py
│       ├── devices.py
│       ├── pipeline.py
│       ├── providers/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── stt/
│       │   │   ├── __init__.py
│       │   │   ├── local.py
│       │   │   └── cloud.py
│       │   ├── llm/
│       │   │   ├── __init__.py
│       │   │   ├── local.py
│       │   │   └── cloud.py
│       │   └── tts/
│       │       ├── __init__.py
│       │       ├── local.py
│       │       └── cloud.py
│       └── logging.py
├── tests/
│   ├── test_state_machine.py
│   ├── test_latency.py
│   ├── test_interfaces.py
│   ├── test_providers.py
│   └── test_pipeline.py
└── docs/
    └── architecture.md
```

## Flujo principal

1. El usuario pulsa push-to-talk.
2. El micrófono captura audio.
3. El proveedor STT transforma audio en texto.
4. El proveedor LLM genera respuesta basada en el texto.
5. El proveedor TTS convierte la respuesta en audio.
6. El altavoz reproduce el audio.

## Contratos de proveedores

Cada proveedor implementa una interfaz compartida:

- `transcribe(audio_bytes) -> str`
- `generate(prompt) -> str`
- `synthesize(text) -> bytes`

La inyección se realiza por composición en el orquestador, no por if/else por toda la app.

## Estados

- `IDLE`
- `LISTENING`
- `PROCESSING`
- `SPEAKING`
- `ERROR`

Cada transición valida que la etapa previa haya terminado bien y registra latencia por etapa.
