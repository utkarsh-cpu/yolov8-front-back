
from flask import Flask, request, flash, redirect, url_for, send_from_directory, jsonify, render_template, make_response
from werkzeug.utils import secure_filename
import os
import requests
from preprocess import preprocess_image

app = Flask(__name__)

AI_BACKEND_URL = os.environ.get('AI_BACKEND_URL', 'http://ai_backend:5001')
IMAGE_FOLDER = "/Users/utkarsh_kaushik/PycharmProjects/flaskProject"
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    # Serve the frontend page
    return render_template('frontend.html')


@app.route('/upload', methods=['POST'])
def upload_image():

    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    img_file = request.files['image']
    filename = img_file.filename
    if not filename:
        filename = 'uploaded.jpg'

    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    temp_input_path = os.path.join(temp_dir, filename)
    img_file.save(temp_input_path)

    # Preprocess: resize to 640x480 for YOLO, etc.
    preprocessed_path = os.path.join(temp_dir, f"preprocessed_{filename}")
    preprocess_image(
        input_path=temp_input_path,
        output_path=preprocessed_path,
        resize=(640,480)
    )

    # Send the preprocessed file to AI backend
    with open(preprocessed_path, 'rb') as f:
        files = {'image': (filename, f, 'image/jpeg')}
        response = requests.post(f"{AI_BACKEND_URL}/detect", files=files)


    if response.status_code == 200:
        # The AI backend's response is already JSON with detections + annotated_image
        return response.text, 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({"error": "AI backend error", "detail": response.text}), response.status_code


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["IMAGE_FOLDER"], name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
