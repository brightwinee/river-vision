from flask import Flask, request, jsonify, render_template, redirect
import cv2
from ultralytics import YOLO
from shapely.geometry import Polygon
from random import randint
import numpy as np
import torch
import time

app = Flask(__name__, template_folder='templates')
model = YOLO('static/best.pt')  # Đường dẫn tới trọng số YOLOv9

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Thực hiện kiểm tra tên người dùng và mật khẩu
    if username == 'admin' and password == 'admin123':
        # Nếu tên người dùng và mật khẩu đúng, chuyển hướng đến trang index.html
        return redirect('/index')
    else:
        # Nếu tên người dùng hoặc mật khẩu không đúng, hiển thị thông báo lỗi
        return render_template('login.html', error='Tên người dùng hoặc mật khẩu không đúng')

@app.route('/index')
def secure_index():
    return render_template('index.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/tool')
def tool():
    return render_template('tool.html')

@app.route('/segment', methods=['POST'])
def segment_image():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    start_time = time.time()
    results = model.predict(source=img, save=False, save_txt=False, stream=True)

    for result in results:
        masks = result.masks.data
        boxes = result.boxes.data
        clss = boxes[:, 5]
        people_indices = torch.where(clss == 0)  # Lớp 0 là sông hồ
        people_masks = masks[people_indices]
        people_mask = torch.any(people_masks, dim=0).int() * 255
        res = people_mask.cpu().numpy()

    sum_pixel = cv2.countNonZero(res)
    area = "{:,}".format(int(sum_pixel * 10 * 10))

    _, encoded_img = cv2.imencode('.png', res)

    end_time = time.time()
    execution_time = round(end_time - start_time, 2)

    response = {'segmented_image': encoded_img.tolist(), 'area': area, 'execution_time': execution_time}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="1450", debug=True)
