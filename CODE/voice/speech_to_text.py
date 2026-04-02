import os
import asyncio
import sounddevice as sd
from scipy.io.wavfile import write
from deepgram import Deepgram
from dotenv import load_dotenv

load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
dg_client = Deepgram(DEEPGRAM_API_KEY)

def record_audio():
    print("🎤 Recording your audio...")
    audio = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    write("mic_input.wav", 16000, audio)
    print("✅ Recording complete. Audio saved as mic_input.wav")

async def transcribe_audio():
    try:
        with open("mic_input.wav", "rb") as audio:
            buffer = audio.read()

        source = {
            "buffer": buffer,
            "mimetype": "audio/wav"
        }

        print("🧠 Transcribing your audio...")
        response = await asyncio.wait_for(
            dg_client.transcription.prerecorded(
                source,
                {"punctuate": True, "model": "nova"}
            ),
            timeout=30  
        )

        transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]

        if not transcript.strip():
            print("❌ No speech detected.")
            return None

        return transcript

    except asyncio.TimeoutError:
        print("Transcription timed out.")
        return None
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return None

async def main():
    record_audio()
    transcript = await transcribe_audio()
    if transcript:
        print("\nTranscription:\n", transcript)
    else:
        print("Could not transcribe your audio.")

if __name__ == "__main__":
    asyncio.run(main())
