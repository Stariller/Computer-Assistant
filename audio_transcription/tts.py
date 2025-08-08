import sounddevice as sd
import numpy as np
from TTS.api import TTS

# Load the Jenny model
tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=True)

def text_to_speech_file(text: str, file_path: str):
    """
    Synthesize speech and save to a file.

    Args:
        text (str): The text to synthesize.
        file_path (str): The path to save the synthesized speech.
    """
    tts.tts_to_file(text=text, file_path=file_path)

def stream_text_to_speech(text: str):
    """
    Synthesize speech from text and stream it to the default sound device.

    Args:
        text (str): The text to synthesize.
    """
    global tts  # Ensure tts object is accessible
    if tts is None:
        print("Error: TTS object is not initialized.")
        return

    try:
        print(f"Synthesizing audio for: \"{text[:50]}...\"")
        # The tts.tts() method returns a list of audio samples (waveform)
        audio_samples = tts.tts(text=text)

        if not audio_samples:
            print("Warning: TTS returned no audio samples.")
            return

        # Convert to NumPy array, ensure float32 for sounddevice
        audio_np = np.array(audio_samples, dtype=np.float32)

        # Get the sample rate from the TTS model
        # For Coqui TTS, this is typically found in tts.synthesizer.output_sample_rate
        samplerate = tts.synthesizer.output_sample_rate

        print(f"Audio synthesized. Sample rate: {samplerate} Hz, Duration: {len(audio_np)/samplerate:.2f}s")
        print("Playing audio...")
        sd.play(audio_np, samplerate)
        sd.wait()  # Wait until playback is finished
        print("Playback finished.")

    except AttributeError as e:
        print(f"Error accessing TTS properties (e.g., sample rate). Make sure your TTS object is standard: {e}")
    except Exception as e:
        print(f"An error occurred during audio streaming: {e}")
