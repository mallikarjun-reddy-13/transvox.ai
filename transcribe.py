import whisper
import os
from moviepy.editor import VideoFileClip

def extract_audio(video_path):
    """Extract audio from video file"""
    audio_path = video_path.replace('.mp4', '.wav').replace('.mov', '.wav').replace('.avi', '.wav')
    audio_path = audio_path.replace('input_video', 'input_video/audio')
    
    # Create audio folder
    os.makedirs('input_video/audio', exist_ok=True)
    
    # Extract audio using moviepy
    video = VideoFileClip(video_path)
    
    if video.audio is None:
        raise Exception("Video has no audio track!")
    
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')
    video.close()
    
    return audio_path

def transcribe_audio(video_path):
    """Transcribe audio from video to text using Whisper"""
    
    # Step 1: Extract audio from video
    print("Extracting audio from video...")
    audio_path = extract_audio(video_path)
    
    # Step 2: Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    # Step 3: Transcribe audio to text
    print("Transcribing audio...")
    result = model.transcribe(audio_path)
    
    text = result["text"]
    print(f"Transcription done: {text}")
    
    return text