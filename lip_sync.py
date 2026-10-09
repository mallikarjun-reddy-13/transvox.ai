import subprocess
import sys
from pathlib import Path

from moviepy.editor import AudioFileClip, VideoFileClip


def sync_lips(video_path, audio_path, filename):
    """Render a dubbed video, using Wav2Lip when its model is installed."""
    video_path = Path(video_path)
    audio_path = Path(audio_path)
    safe_stem = video_path.stem
    if len(safe_stem) != 32 or any(char not in "0123456789abcdef" for char in safe_stem):
        raise ValueError("Invalid internal video filename.")

    output_dir = Path("output_video")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{safe_stem}_dubbed.mp4"

    wav2lip_script = Path("Wav2Lip") / "inference.py"
    checkpoint = Path("Wav2Lip") / "checkpoints" / "wav2lip_gan.pth"

    if wav2lip_script.is_file() and checkpoint.is_file():
        command = [
            sys.executable, str(wav2lip_script),
            "--checkpoint_path", str(checkpoint),
            "--face", str(video_path),
            "--audio", str(audio_path),
            "--outfile", str(output_path),
        ]
        subprocess.run(command, check=True)
        if not output_path.is_file():
            raise RuntimeError("Wav2Lip did not create the output video.")
        return str(output_path)

    print("Wav2Lip script/checkpoint not found; replacing the audio track only.")
    video = VideoFileClip(str(video_path))
    new_audio = AudioFileClip(str(audio_path))
    final_video = None
    try:
        final_video = video.set_audio(new_audio)
        final_video.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            logger=None,
        )
    finally:
        if final_video is not None:
            final_video.close()
        new_audio.close()
        video.close()

    return str(output_path)
