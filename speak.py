# speak.py

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=api_key)

def play_response(text):
    voice_id = "goT3UYdM9bhm0n2lmKQx"
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text
    )
    play(audio)
    output_path = "audio/output.mp3"
    save(audio, output_path)

    return output_path
