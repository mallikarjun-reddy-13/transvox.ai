from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Folders
INPUT_FOLDER = 'input_video'
OUTPUT_FOLDER = 'output_video'
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('.', 'transvox.html')

# Upload video
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filepath = os.path.join(INPUT_FOLDER, file.filename)
    file.save(filepath)

    return jsonify({'message': 'Video uploaded successfully', 'filename': file.filename})

# Process video
@app.route('/process', methods=['POST'])
def process_video():
    data = request.json
    filename = data.get('filename')
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'te')

    input_path = os.path.join(INPUT_FOLDER, filename)

    if not os.path.exists(input_path):
        return jsonify({'error': 'Video not found'}), 404

    try:
        # Step 1: Transcribe
        from transcribe import transcribe_audio
        print("Step 1: Transcribing audio...")
        text = transcribe_audio(input_path)
        print(f"Transcribed: {text}")

        # Step 2: Translate
        from translate import translate_text
        print("Step 2: Translating text...")
        translated_text = translate_text(text, source_lang, target_lang)
        print(f"Translated: {translated_text}")

        # Step 3: Voice Clone
        from voice_clone import clone_voice
        print("Step 3: Cloning voice...")
        audio_path = clone_voice(translated_text, filename)
        print(f"Voice cloned: {audio_path}")

        # Step 4: Lip Sync
        from lip_sync import sync_lips
        print("Step 4: Syncing lips...")
        output_path = sync_lips(input_path, audio_path, filename)
        print(f"Lip sync done: {output_path}")

        return jsonify({
            'message': 'Processing complete!',
            'output': os.path.basename(output_path)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Download output video
@app.route('/download/<filename>')
def download_video(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    print("TransVox Server Starting...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
