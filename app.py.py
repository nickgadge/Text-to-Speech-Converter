from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['AUDIO_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'audio')

# Ensure audio directory exists
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    # Clean up old files (keep last 5)
    audio_files = sorted(os.listdir(app.config['AUDIO_FOLDER']))
    for old_file in audio_files[:-5]:
        os.remove(os.path.join(app.config['AUDIO_FOLDER'], old_file))
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']

    if not text.strip():
        return jsonify({'status': 'error', 'message': 'Please enter text'})

    try:
        process = subprocess.Popen(
            ['python', 'text_to_speech.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=text)

        if process.returncode == 0:
            filename = stdout.strip()
            if filename and filename != "ERROR":
                return jsonify({
                    'status': 'success',
                    'filename': filename,
                    'download_url': f'/download/{filename}',
                    'play_url': f'/static/audio/{filename}'
                })
        return jsonify({'status': 'error', 'message': stderr or 'Conversion failed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/download/<filename>')
def download(filename):
    safe_filename = secure_filename(filename)
    filepath = os.path.join(app.config['AUDIO_FOLDER'], safe_filename)

    if not os.path.exists(filepath):
        return "File not found", 404

    return send_from_directory(
        app.config['AUDIO_FOLDER'],
        safe_filename,
        as_attachment=True,
        mimetype='audio/mpeg'
    )

@app.route('/static/audio/<filename>')
def serve_audio(filename):
    safe_filename = secure_filename(filename)
    filepath = os.path.join(app.config['AUDIO_FOLDER'], safe_filename)

    if not os.path.exists(filepath):
        return "File not found", 404

    return send_from_directory(
        app.config['AUDIO_FOLDER'],
        safe_filename,
        mimetype='audio/mpeg'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
