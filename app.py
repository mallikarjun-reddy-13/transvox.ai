import os
import re
import uuid
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 MB

INPUT_FOLDER = Path("input_video")
OUTPUT_FOLDER = Path("output_video")
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".avi"}
SAFE_FILENAME = re.compile(r"^[a-f0-9]{32}\.(mp4|mov|avi)$")

INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


@app.errorhandler(RequestEntityTooLarge)
def handle_large_upload(_error):
    return jsonify({"error": "Video is too large. Maximum upload size is 500 MB."}), 413


@app.route("/")
def index():
    return send_from_directory(".", "transvox.html")


@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video file was provided."}), 400

    uploaded_file = request.files["video"]
    if not uploaded_file.filename:
        return jsonify({"error": "Please select a video file."}), 400

    extension = Path(uploaded_file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file type. Upload MP4, MOV, or AVI."}), 415

    # Never use a client-supplied filename as a filesystem path.
    safe_filename = f"{uuid.uuid4().hex}{extension}"
    destination = INPUT_FOLDER / safe_filename
    uploaded_file.save(destination)

    return jsonify({
        "message": "Video uploaded successfully.",
        "filename": safe_filename,
    }), 201


@app.route("/process", methods=["POST"])
def process_video():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    filename = data.get("filename")
    if not isinstance(filename, str) or not SAFE_FILENAME.fullmatch(filename):
        return jsonify({"error": "Invalid video filename. Please upload the video again."}), 400

    source_lang = data.get("source_lang", "en")
    target_lang = data.get("target_lang", "te")
    supported_languages = {"en", "hi", "ta", "kn", "mr", "bn", "te"}

    if source_lang not in supported_languages or target_lang not in supported_languages:
        return jsonify({"error": "Unsupported language selection."}), 400
    if source_lang == target_lang:
        return jsonify({"error": "Choose different source and target languages."}), 400

    input_path = INPUT_FOLDER / filename
    if not input_path.is_file():
        return jsonify({"error": "Uploaded video was not found. Please upload it again."}), 404

    try:
        from transcribe import transcribe_audio
        from translate import translate_text
        from voice_clone import clone_voice
        from lip_sync import sync_lips

        print("Step 1: Transcribing audio...")
        transcribed_text = transcribe_audio(str(input_path))
        if not transcribed_text or not transcribed_text.strip():
            return jsonify({"error": "No speech could be transcribed from this video."}), 422

        print("Step 2: Translating text...")
        translated_text = translate_text(transcribed_text, source_lang, target_lang)
        if not translated_text or not translated_text.strip():
            return jsonify({"error": "Translation returned no text."}), 502

        print("Step 3: Generating dubbed audio...")
        audio_path = clone_voice(translated_text, filename)

        print("Step 4: Rendering video...")
        output_path = sync_lips(str(input_path), audio_path, filename)

        if not Path(output_path).is_file():
            raise RuntimeError("Video processing finished without creating an output file.")

        return jsonify({
            "message": "Processing complete.",
            "output": Path(output_path).name,
        })

    except Exception:
        # Keep detailed exception data in server logs, not in public responses.
        app.logger.exception("Video processing failed")
        return jsonify({
            "error": "Video processing failed. Check the server logs for details and verify your API key, FFmpeg, and model files.",
        }), 500


@app.route("/download/<path:filename>")
def download_video(filename):
    if not isinstance(filename, str) or not re.fullmatch(r"[a-f0-9]{32}_(dubbed)\.mp4", filename):
        return jsonify({"error": "Invalid output filename."}), 400
    if not (OUTPUT_FOLDER / filename).is_file():
        return jsonify({"error": "Output video not found."}), 404
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    print("TransVox server starting. Open http://localhost:5000")
    # Debug mode is intentionally disabled to avoid exposing the debugger.
    app.run(host="127.0.0.1", port=5000, debug=False)
