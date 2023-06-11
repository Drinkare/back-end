from ultralytics import YOLO
import torch
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

UPLOAD_FOLDER = './data'  # Update path as necessary
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/test', methods=['POST'])
def test():
    tori = {'tori':'tori is best'}
    return jsonify(tori)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        resp = Response('No image part in the request.')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 400

    file = request.files['image']

    if file.filename == '':
        resp = Response('No selected image.')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = Response('Image uploaded successfully.')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp, 200

    resp = Response('Invalid image.')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp, 400 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
