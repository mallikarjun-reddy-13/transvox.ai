import os
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()


def clone_voice(text, filename):
    """Generate translated speech using the configured ElevenLabs voice."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is missing. Add it to your local .env file.")

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Cannot generate audio from empty text.")

    # app.py only accepts server-generated UUID filenames.
    safe_stem = Path(filename).stem
    if len(safe_stem) != 32 or any(char not in "0123456789abcdef" for char in safe_stem):
        raise ValueError("Invalid internal filename.")

    audio_dir = Path("input_video") / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_output_path = audio_dir / f"{safe_stem}_translated.mp3"

    client = ElevenLabs(api_key=api_key)
    audio_chunks = client.text_to_speech.convert(
        voice_id=os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb"),
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with audio_output_path.open("wb") as output_file:
        for chunk in audio_chunks:
            output_file.write(chunk)

    if audio_output_path.stat().st_size == 0:
        audio_output_path.unlink(missing_ok=True)
        raise RuntimeError("The voice provider returned an empty audio file.")

    return str(audio_output_path)
