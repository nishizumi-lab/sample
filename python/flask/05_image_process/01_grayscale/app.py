from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
from datetime import datetime as dt

app = Flask(__name__, static_url_path="")

# 処理した画像ファイルの保存先
IMG_DIR = "/static/images/"
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = BASE_DIR + IMG_DIR

# 保存先のパスがなければ作成
if not os.path.isdir(IMG_PATH):
    os.mkdir(IMG_PATH)

# グレースケール変換
def rgb_to_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


@app.route('/', methods=['GET', 'POST'])
def index():
    img_name = ""

    if request.method == 'POST':
        # 画像をロード
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

        # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            img = cv2.imdecode(img_array, 1)
            # グレースケール変換
            gray = rgb_to_gray(img)
            now_date = dt.now()
            img_name = "gray" + now_date.strftime('%Y-%m-%d-%H-%M-%S') + ".png"
            # 画像の保存
            cv2.imwrite(os.path.join(IMG_PATH + img_name), gray)


    return render_template('index.html', img_name=img_name)


if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)
