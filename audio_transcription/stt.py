import os
os.environ["LD_PRELOAD"] = "/usr/lib/x86_64-linux-gnu/libstdc++.so.6"

import sounddevice as sd
import queue
import sys
import json
import time
from vosk import Model, KaldiRecognizer

def audio_transcribe(model_path: str, sample_rate: int) -> str:
    """
    Starts real-time audio transcription using the Vosk model.

    Args:
        model_path (str): Path to the Vosk model directory.
        sample_rate (int): Audio sample rate (e.g., 16000).
    Returns:
        str: The full transcription as a single string after the session ends.
    """
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)
    rec.SetWords(True)
    
    # Silence-based auto-stop parameters
    silence_timeout = 1.2  # seconds of silence to stop listening
    speech_started = False
    last_voice_time = None
    
    # Create a queue and callback to receive audio from the input stream
    q = queue.Queue()
    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        # Convert to bytes for Vosk recognizer
        q.put(bytes(indata))

    transcription = []  # Accumulate recognized text here
    with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("Listening... (Press Ctrl+C to exit)")
        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        transcription.append(text)
                        speech_started = True
                        last_voice_time = time.time()
                else:
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "")
                    if partial_text:
                        speech_started = True
                        last_voice_time = time.time()
                    print("Partial:", partial_text, end='\r')

                # Stop after a short period of silence once speech has started
                if speech_started and last_voice_time is not None:
                    if time.time() - last_voice_time > silence_timeout:
                        break
            
            # Finalize any remaining audio in the recognizer and print completion
            final_result = json.loads(rec.FinalResult())
            final_text = final_result.get("text", "")
            if final_text:
                transcription.append(final_text)
            print("\nTranscription completed.")
        except KeyboardInterrupt:
            # Propagate Ctrl+C so the main loop can exit immediately
            print("\nTranscription interrupted by user.")
            raise
        except Exception as e:
            print(f"Error: {e}")
    # Return the full transcription as a single string
    return " ".join(transcription)
