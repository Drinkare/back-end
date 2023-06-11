from flask import Flask, jsonify, request, send_file
from ultralytics import YOLO
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import json
import base64
import shutil
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER ='/home/ubuntu/ultralytics/data'
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
    print(request.data)
    print(request.files)
    print(request.form)
    if 'image' not in request.files:
        return 'No image part in the request.', 400

    file = request.files['image']

    if file.filename == '':
        return 'No selected image', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        model = YOLO('best.pt')
        #model = YOLO('/content/ultralytics/runs/detect/train/weights/best.pt')  # load a custom model
        results = model.predict(source='data/'+filename,save=True, imgsz=640, conf=0.3,project="zzz",name="SSS")
        counts={}
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                cls = int(box.cls[0])
                if not cls in counts.keys():
                    counts[cls] = 1
                else:
                    counts[cls] += 1

        dic = {
            "soju": 0,
            "person": 0,
            "beer": 0,
            "jinro":0,
            "cass":0,
            "terra":0,
            "cass-can":0
        }
        for key in counts.keys():
            print(model.names[key] + " : " + str(counts[key]))
            dic[model.names[key]] = counts[key]
        model = YOLO('yolov8n.pt')
        results = model.predict(source='./zzz/SSS/'+filename,classes=0,save=True, imgsz=640, conf=0.3,project="zzz2",name="SSS2")
        image_file = FileStorage('./zzz2/SSS2/'+filename)
        
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                cls = int(box.cls[0])
                if not cls in counts.keys():
                    counts[cls] = 1
                else:
                    counts[cls] += 1


        for key in counts.keys():
            if model.names[key] != 'person':
                continue
            print(model.names[key] + " : " + str(counts[key]))
            dic[model.names[key]] = counts[key]
        print(dic)
            
        dic['beer'] = dic.get('cass',0)+dic.get('terra',0)+dic.get('cass-can',0)
        dic['soju'] = dic.get('jinro',0)+dic.get('soju',0)
        del dic['jinro']
        del dic['cass']
        del dic['terra']
        del dic['cass-can']
        with open('./zzz2/SSS2/'+filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
        response = {
            'image': encoded_string,
            'data': dic
        }
        print("done")

        dir_path = "./zzz"
        dir_path2 = "./zzz2"

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        if os.path.exists(dir_path2):
            shutil.rmtree(dir_path2)
        os.remove('./data/'+filename)
        return jsonify(response)
#        return send_file(image_file, mimetype= 'image/jpg')
    return 'Invalid image', 400

'''
        import os
        import shutil

        dir_path = "./zzz"
        dir_path2 = "./zzz2"

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        if os.path.exists(dir_path2):
            shutil.rmtree(dir_path2)
'''

        # Get the JSON data
     #   if 'json' not in request.form:
         #   return 'No JSON part in the request.', 400

        #jsonDataStr = request.form['json']
        #jsonData = json.loads(jsonDataStr)  # Convert string back to JSON
        
        # Do something with the JSON data...
        
       # return 'Image and JSON uploaded successfully', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

