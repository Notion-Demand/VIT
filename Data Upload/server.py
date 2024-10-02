import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200

@app.route('/upload-url', methods=['POST'])
def upload_from_url():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
        file_content = response.text

        # Determine file type based on content or URL extension
        filename = url.split('/')[-1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        with open(filepath, 'w') as f:
            f.write(file_content)

        return jsonify({"message": "File from URL saved successfully", "filename": filename}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
