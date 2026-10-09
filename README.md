TransVox - AI Video Dubbing Engine

## Purpose

TransVox is an AI powered video dubbing tool.
It converts any video from one language to another
with same voice and perfect lip sync.

---

## Supported Languages
- English to Telugu

---

## Requirements
- Python 3.10
- VS Code
- Internet Connection
- ElevenLabs API Key (free tier)
- Google Colab (for Lip Sync - no GPU needed)

---

## AI Tools Used
- OpenAI Whisper - Speech to Text (voice ni text ga convert chestundi)
- Google Translate API - Text Translation (English to Telugu translate chestundi)
- ElevenLabs - Voice Cloning (same voice tho Telugu lo matladistundi)
- Wav2Lip - Lip Sync (lips ni new audio ki match chestundi)

---

## Tech Stack
- Python 3.10 - Main programming language
- Flask - Backend server
- FFmpeg - Video and audio processing
- HTML CSS JS - Frontend UI
- Virtual Environment (venv) - Project environment

---

## Project Structure
```
TransVox/
├── transvox.html        - Frontend UI
├── app.py               - Flask Backend
├── transcribe.py        - Whisper Speech to Text
├── translate.py         - Google Translate
├── voice_clone.py       - ElevenLabs Voice Clone
├── lip_sync.py          - Wav2Lip Lip Sync
├── requirements.txt     - Python Libraries
├── .env                 - API Keys (secret)
└── README.md            - This file
```

---

## Installation Steps
1. Install Python 3.10
2. Install VS Code
3. Open TransVox folder in VS Code
4. Create Virtual Environment:
   python -m venv venv
5. Activate Virtual Environment:
   venv\Scripts\activate
6. Install Libraries:
   pip install -r requirements.txt
7. Add API Keys in .env file:
   ELEVENLABS_API_KEY=your_key_here
8. Run the app:
   python app.py
9. Open browser:
   http://localhost:5000

---

## How to Use
1. Upload your video (MP4, MOV, AVI)
2. Select source language (English, Hindi, Tamil...)
3. Select target language (Telugu...)
4. Enable Voice Clone, Lip Sync options
5. Click Start TransVox
6. Wait for processing
7. Download your dubbed video

---

## How It Works
Video → Whisper → Google Translate → ElevenLabs → Wav2Lip → Final Video
(audio)  (text)    (telugu text)     (telugu audio)  (lip sync)

---

## Future Features
- Batch video processing
- More language support
- Custom voice upload
- Mobile app
- Cloud deployment

---

## Developer
Built by - Mallikarjun reddy 
Project - TransVox
Version - 1.0.0
