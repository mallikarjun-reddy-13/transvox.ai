from pathlib import Path

import whisper
from moviepy.editor import VideoFileClip


def extract_audio(video_path):
    """Extract a video's audio track into a WAV file."""
    video_path = Path(video_path)
    audio_dir = Path("input_video") / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_path = audio_dir / f"{video_path.stem}.wav"

    video = VideoFileClip(str(video_path))
    try:
        if video.audio is None:
            raise ValueError("This video does not contain an audio track.")
        video.audio.write_audiofile(
            str(audio_path),
            codec="pcm_s16le",
            logger=None,
        )
    finally:
        video.close()

    return str(audio_path)


def transcribe_audio(video_path):
    """Extract audio from a video and transcribe it with Whisper."""
    audio_path = extract_audio(video_path)
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return (result.get("text") or "").strip()
    finally:
        # Keep intermediate audio only for the duration of transcription.
        Path(audio_path).unlink(missing_ok=True)
