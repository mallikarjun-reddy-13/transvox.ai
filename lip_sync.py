import os
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip

def sync_lips(video_path, audio_path, filename):
    """Sync lips in video with new translated audio"""
    
    print("Starting lip sync process...")
    
    # Output path
    os.makedirs('output_video', exist_ok=True)
    output_path = f"output_video/{filename}_dubbed.mp4"
    
    # Check if Wav2Lip is available
    wav2lip_path = "Wav2Lip/inference.py"
    
    if os.path.exists(wav2lip_path):
        # Use Wav2Lip for proper lip sync
        print("Using Wav2Lip for lip sync...")
        output_path = run_wav2lip(video_path, audio_path, output_path)
    else:
        # Simple audio replacement (without lip sync)
        print("Wav2Lip not found - Using simple audio replacement...")
        output_path = replace_audio(video_path, audio_path, output_path)
    
    print(f"Lip sync complete: {output_path}")
    return output_path

def replace_audio(video_path, audio_path, output_path):
    """Replace video audio with translated audio"""
    
    print("Replacing audio in video...")
    
    # Load video and new audio
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(audio_path)
    
    # Replace audio
    final_video = video.set_audio(new_audio)
    
    # Save final video
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac'
    )
    
    # Close files
    video.close()
    new_audio.close()
    final_video.close()
    
    print(f"Audio replaced successfully: {output_path}")
    return output_path

def run_wav2lip(video_path, audio_path, output_path):
    """Run Wav2Lip for proper lip sync"""
    
    print("Running Wav2Lip...")
    
    command = [
        "python", "Wav2Lip/inference.py",
        "--checkpoint_path", "Wav2Lip/checkpoints/wav2lip_gan.pth",
        "--face", video_path,
        "--audio", audio_path,
        "--outfile", output_path
    ]
    
    subprocess.run(command, check=True)
    
    print(f"Wav2Lip complete: {output_path}")
    return output_path