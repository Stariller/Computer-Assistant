from audio_transcription.stt import audio_transcribe
from audio_transcription.tts import stream_text_to_speech
from llm.agents import main_agent
from llm.session import create_session, create_runner, run_conversation
import asyncio
from google.adk.runners import Runner

WAKE_WORD = "computer"

# Constants for testing
APP_NAME = "Computer Assistant"
USER_ID = "user_1"
SESSION_ID = "session_001"

def send_to_llm(message: str, runner: Runner, user_id: str, session_id: str) -> None:
    """
    Sends the message to the LLM.
    
    Args:
        message (str): The message to send to the LLM.
    """
    print("Sending to LLM:", message)
    result = asyncio.run(run_conversation(message, runner, user_id, session_id))
    print("LLM response:", result)
    stream_text_to_speech(result)

if __name__ == "__main__":
    MODEL_PATH = "./audio_transcription/vosk-model-small-en-us-0.15"
    SAMPLE_RATE = 16000 

    session = asyncio.run(create_session(APP_NAME, USER_ID, SESSION_ID))
    runner = create_runner(main_agent, APP_NAME, session)

    try:
        while True:
            full_message = audio_transcribe(MODEL_PATH, SAMPLE_RATE)
            
            print("Full message:", full_message)
            if full_message and WAKE_WORD in full_message.lower():
                send_to_llm(full_message, runner, USER_ID, SESSION_ID)
            else:
                print(f"Wake word '{WAKE_WORD}' not detected; waiting for next utterance.")
    except KeyboardInterrupt:
        print("\nShutting down. Goodbye.")

    # NOTE: For DEBUG; bypass the audio transcription and send a message directly to the LLM.
    # send_to_llm("Write a python script and save the script to a .py file.", runner, USER_ID, SESSION_ID)
