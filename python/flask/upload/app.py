from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
from image_process import rgb_to_gray
from datetime import datetime
import os
import string
import random

SAVE_DIR = "./images/"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")


@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])


@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
    #if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            img = cv2.imdecode(img_array, 1)
            # グレースケール変換
            gray = rgb_to_gray(img)
            # 画像の保存
            save_path = os.path.join(SAVE_DIR + "gray.png")
            cv2.imwrite(save_path, gray)

        return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run()
