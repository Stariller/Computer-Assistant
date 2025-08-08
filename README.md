# Important!
Run only within a sandbox environment. This has tool capability with the command line and has the potential to cause unknown damange.

# Computer Assistant (Voice-Based)

A small voice assistant that listens via Vosk STT, routes requests to an LLM using Google's Agent Development Kit (ADK), and replies with speech via Coqui TTS.

- STT: Vosk (offline speech-to-text)
- Orchestration: Google ADK with a main agent and a coder sub-agent
- LLM model (via ADK): `openai/gpt-oss:20b` (configurable)
- TTS: Coqui `TTS` Jenny model

This project was only tested on Linux systems.

## Quick start

Prereqs:
- Python 3.10+
- Ollama installed and running on port 11434
- Linux with audio support (See TTS / STT Notes)
- System packages (Ubuntu/Debian):
  - `sudo apt-get update && sudo apt-get install -y libportaudio2`

Setup:
```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download default ollama model
ollama pull gpt-oss:20b

# Download default vosk model
mkdir -p Computer_Assistant/audio_transcription
cd Computer_Assistant/audio_transcription
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip -q vosk-model-small-en-us-0.15.zip

# Weather API
export WEATHER_API_KEY="<your_weatherapi_key>"  # https://www.weatherapi.com/

# Run application
python main.py
```

Environment variables:
```bash
# Required for weather tools
export WEATHER_API_KEY="<your_weatherapi_key>"  # https://www.weatherapi.com/
```

By default the app uses:
- Wake word: `computer`
- App name: `Computer Assistant`
- Vosk model path: `./audio_transcription/vosk-model-small-en-us-0.15`

## Project structure
```
Computer_Assistant/
  main.py                      # App entrypoint
  audio_transcription/
    stt.py                     # Speech-to-text (Vosk)
    tts.py                     # Text-to-speech (Coqui TTS)
  llm/
    agents.py                  # ADK agent graph (main + coder sub-agent)
    session.py                 # Session & runner helpers
    tools/tools.py             # Utility tools (time/date/weather/city, CLI)
```

## Wake word behavior
Send the wake word to the LLM; defined in `main.py` as `WAKE_WORD = "computer"`. This will be what sends your message to the LLM to be processed.

## Notes on ADK / Ollama
This sample uses Google ADK (`google-adk`). Make sure it installs cleanly via pip (see `requirements.txt`). This makes calls to Ollama on port 11434.
You are able to use any tool equiped model available from Ollama. See https://ollama.com/ to download and install Ollama.

## Notes on TTS / STT 
- `sounddevice` errors: install `libportaudio2` (Debian/Ubuntu). On other distros, install the equivalent PortAudio package.
- Coqui TTS GPU: the code requests `gpu=True`. If you don’t have a GPU, set it to `False` in `tts.py`.
- Vosk model not found: verify `MODEL_PATH` in `main.py` and the folder name you unzipped. Model used: `vosk-model-small-en-us-0.15`
    see https://github.com/alphacep/vosk-tts for more information.
- For more Coqui TTS information see https://github.com/coqui-studio/TTS. Our default model is `Jenny`.

## About OpenAI through Google ADK
Google ADK doesn't allow Ollama's wrapper to use tools. Instead the wrapper for openai was used. There are environment variables to set the endpoint to the ollama server, with an api key that is only a placeholder. This is a workaround to allow the ollama models to be used as intended with Google ADK.
