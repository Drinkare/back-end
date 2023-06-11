
from ultralytics import YOLO
import torch
#device = torch.device('mps:0' if torch.backends.mps.is_available() else 'cpu')
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/test')#, #methods=['POST'])
def test():
    #param = request.get_json()
    model = YOLO('best.pt')
    #model = YOLO('/content/ultralytics/runs/detect/train/weights/best.pt')  # load a custom model
    model.predict(source='file6.jpg',save=True, imgsz=640, conf=0.3,project="zzz",name="SSS")
    #model = YOLO('yolov8n.pt')
    #result1=model.predict(source='./zzz/SSS/data1.jpg',classes=0,save=True, imgsz=640, conf=0.3,project="zzz2",name="SSS2")
    #tori = {tori:'tori is best'}
    return 'aaaaaa'#jsonify(tori)

# 파이썬 명령어로 실행할 수 있음
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)




#TODO
'''
#사진 리턴 후 폴더삭제
import os
import shutil

dir_path = "./zzz"
dir_path2 = "./zzz2"

if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
if os.path.exists(dir_path2):
    shutil.rmtree(dir_path2)
    '''

