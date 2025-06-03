from flask import Flask, request, jsonify, send_file
from assistant import handle_request
import os

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("input")
    thread_id = data.get("thread_id")

    reply, thread_id, audio_path = handle_request(user_input, thread_id)

    return jsonify({
        "reply": reply,
        "thread_id": thread_id,
        "audio_file": f"/audio/{os.path.basename(audio_path)}"
    })

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_file(
        os.path.join("audio", filename),
        mimetype="audio/mpeg"
    )

if __name__ == "__main__":
    os.makedirs("audio", exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))