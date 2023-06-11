from ultralytics import YOLO
import torch
#device = torch.device('mps:0' if torch.backends.mps.is_available() else 'cpu')
from flask import Flask, jsonify, request,Response
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})

UPLOAD_FOLDER ='./data'#폴더경로 수정필

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/test', methods=['POST'])
def test():
    #param = request.get_json()
    #model = YOLO('best.pt')
    #model = YOLO('/content/ultralytics/runs/detect/train/weights/best.pt')  # load a custom model
    #model.predict(source='file6.jpg',save=True, imgsz=640, conf=0.3,project="zzz",name="SSS")
    #model = YOLO('yolov8n.pt')
    #result1=model.predict(source='./zzz/SSS/data1.jpg',classes=0,save=True, imgsz=640, conf=0.3,project="zzz2",name="SSS2")
    tori = {'tori':'tori is best'}
    return jsonify(tori)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    #print(request.data)
   #print(request.FILES)
    print(request.files)
    print(request.values)
    
    #file = request.files['image']
    #resp=Response("foo bar azzz")
    #resp.headers['Access-Control-Allow-Origin']='*'
    #return resp
    if 'image' not in request.files:
        resp=Response('tori')
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp#'No image part in the request a a a a a a ', 402
    
    file = request.files['image']

    if file.filename == '':
        resp=Response("no image part")
        resp.headers['Access-Control-Allow-Origin']='*'
        return resp#'No selected image', 403

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Image uploaded successfully', 200

    return 'Invalid image', 400

'''    if 'file' not in request.files:
        return 'No file part in the request.', 400

    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file.', 400

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Image has been uploaded.', 200
    
    return 'Invalid image', 400
'''
# 파이썬 명령어로 실행할 수 있음
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
'''

#from flask import Flask, request
#from werkzeug.utils import secure_filename
#import os

#app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/ultralytics/data' # update with your directory

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part in the request', 400

    file = request.files['image']

    if file.filename == '':
        return 'No selected image', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Image uploaded successfully', 200

    return 'Invalid image', 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
'''
