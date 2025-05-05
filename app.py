from flask import Flask, request, jsonify, send_from_directory
import os
import random
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
LOGS_FOLDER = 'logs'
ALLOWED_EXTENSIONS = {'h5', 'tflite', 'onnx'}  # Example model file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['LOGS_FOLDER'] = LOGS_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)


# Utility functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Routes
@app.route('/api/system-status', methods=['GET'])
def system_status():
    """Simulate system status data."""
    return jsonify({
        'device': 'Jetson Nano',
        'temperature': f"{random.randint(30, 70)}°C",  # Fake temperature
        'memory': f"{random.randint(50, 90)}%"  # Fake memory usage
    })


@app.route('/api/upload-model', methods=['POST'])
def upload_model():
    """Handle model upload."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'Model uploaded successfully', 'filename': filename}), 200
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/api/models', methods=['GET'])
def list_models():
    """List uploaded models."""
    models = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'models': models})


@app.route('/api/infer', methods=['POST'])
def infer():
    """Simulate model inference."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    # Simulate an inference result
    label = random.choice(['Cat', 'Dog', 'Car', 'Tree'])
    confidence = random.uniform(0.5, 1.0)
    return jsonify({'label': label, 'confidence': confidence})


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Fetch logs."""
    logs = [
        "[INFO] System started.",
        "[WARNING] High temperature detected.",
        "[INFO] Model inference completed.",
    ]
    return jsonify({'logs': logs})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)