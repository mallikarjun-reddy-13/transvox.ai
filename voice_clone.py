import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing ELEVENLABS_API_KEY in .env")

print("ELEVENLABS_API_KEY loaded:", "YES")

def clone_voice(text, filename):
    """Convert translated text to audio using ElevenLabs"""
    
    print("Connecting to ElevenLabs...")
    
    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=API_KEY)
    
    # Output audio path
    os.makedirs('input_video/audio', exist_ok=True)
    audio_output_path = f"input_video/audio/{filename}_translated.mp3"
    
    print("Generating voice...")
    
    # Generate audio from text
    audio = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # Default voice - George
        text=text,
        model_id="eleven_multilingual_v2",  # Supports Telugu
        output_format="mp3_44100_128"
    )
    
    # Save audio file
    with open(audio_output_path, 'wb') as f:
        for chunk in audio:
            f.write(chunk)
    
    print(f"Voice generated: {audio_output_path}")
    
    return audio_output_path