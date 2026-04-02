import os
import uuid
import requests
import sounddevice as sd
import soundfile as sf
import time
from dotenv import load_dotenv

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

DEFAULT_VOICE = "aura-asteria-en"

def text_to_speech(text: str, voice: str = DEFAULT_VOICE) -> str:
    if not text.strip():
        print("No text provided for TTS.")
        return ""

    print(f"Generating speech: '{text.strip()}'")
    
    url = f"https://api.deepgram.com/v1/speak?voice={voice}"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }

    output_file = f"{uuid.uuid4()}.wav"
    try:
        response = requests.post(url, headers=headers, json={"text": text}, timeout=20)
        if response.status_code == 200 and response.content:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Speech generated and saved to '{output_file}'")
            play_audio(output_file)
            return output_file
        else:
            print(f"TTS failed [{response.status_code}]: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return ""

def play_audio(file_path: str):
    try:
        data, samplerate = sf.read(file_path, dtype='int16')
        sd.play(data, samplerate)
        sd.wait()
        time.sleep(0.5) 
        print("Playback finished.")
    except Exception as e:
        print(f"Playback error: {e}")

if __name__ == "__main__":
    text_to_speech("Hello, this is a test of Deepgram text to speech.")
