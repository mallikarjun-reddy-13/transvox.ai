# TransVox — AI Video Dubbing Engine

TransVox is a Flask-based prototype that transcribes video speech, translates the text, generates translated speech with ElevenLabs, and renders a dubbed video. Lip-sync is performed by Wav2Lip only when its script and checkpoint are installed; otherwise the app replaces the video's audio track.

## Current pipeline

1. Extract audio from the uploaded video.
2. Transcribe speech with OpenAI Whisper.
3. Translate the transcript with `deep-translator` / Google Translate.
4. Generate translated speech with ElevenLabs.
5. Use Wav2Lip when available, or replace the original audio track as a fallback.

**Important:** The configured ElevenLabs voice is a selected provider voice by default. This implementation does not clone the original speaker's voice. Do not describe output as perfect lip-sync unless you have tested that result with Wav2Lip and the required model checkpoint.

## Supported input formats

- MP4
- MOV
- AVI
- Maximum upload size: 500 MB

The language selectors include English, Hindi, Tamil, Kannada, Marathi, Bengali, and Telugu. Provider support and transcription quality can vary. The application currently rejects selecting the same source and target language.

## Requirements

- Python 3.10 (recommended for this dependency set)
- FFmpeg installed and available on PATH
- ElevenLabs API key
- Wav2Lip repository and checkpoint, if you want model-based lip-sync
- A working internet connection for Whisper model download and translation / speech services

## Setup (Windows)

1. Install Python 3.10 and FFmpeg.
2. Clone this repository and open the folder in VS Code.
3. Create and activate a virtual environment:

   ```powershell
   py -3.10 -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Create a local `.env` file in the project root:

   ```dotenv
   ELEVENLABS_API_KEY=your_key_here
   # Optional: set a voice ID you are authorized to use
   ELEVENLABS_VOICE_ID=your_voice_id
   ```

   Never commit real credentials. The `.env` file is excluded by `.gitignore`.

6. Start the server:

   ```powershell
   python app.py
   ```

7. Open http://127.0.0.1:5000 in your browser.

## Project structure

```text
transvox.ai/
├── app.py
├── transvox.html
├── transcribe.py
├── translate.py
├── voice_clone.py
├── lip_sync.py
├── requirements.txt
├── .gitignore
└── README.md
```

The application creates `input_video/` and `output_video/` at runtime. Uploaded videos and rendered outputs are stored on the server; delete them when they are no longer needed. Do not deploy this prototype publicly without adding authentication, rate limits, background jobs, retention cleanup, and production server configuration.

## Security and operational notes

- Uploads are restricted to MP4, MOV, and AVI extensions and a 500 MB request limit. Extension checks are not a substitute for validating actual media contents.
- Flask debug mode is disabled.
- API keys must remain in environment variables and must never be printed or committed.
- Long-running Whisper and video-rendering jobs run in the request handler; a production deployment should use a background job queue and report real progress.
- The app currently runs on localhost by default. Configure a production WSGI server and appropriate network controls before exposing it.

## Troubleshooting

- **MoviePy import errors:** This project pins MoviePy 1.0.3 to match the `moviepy.editor` imports.
- **FFmpeg errors:** Install FFmpeg and confirm `ffmpeg -version` works in the same terminal.
- **ElevenLabs errors:** Confirm the API key is valid and your account has access to the selected model / voice.
- **Lip-sync fallback:** Ensure both `Wav2Lip/inference.py` and `Wav2Lip/checkpoints/wav2lip_gan.pth` exist. Otherwise the app only replaces the audio track.
- **No speech detected:** Use a video with a clear audio track and audible speech.

## Developer

Built by Mallikarjun Reddy Chilakala  
Project: TransVox  
Version: 1.0.0
