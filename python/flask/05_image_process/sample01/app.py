from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import numpy as np
import cv2
from grayscale import rgb_to_gray

app = Flask(__name__, static_url_path="")

# 処理した画像ファイルの保存先
IMG_DIR = "/static/images/"
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = BASE_DIR + IMG_DIR

# 保存先のパスがなければ作成
if not os.path.isdir(IMG_PATH):
    os.mkdir(IMG_PATH)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 画像をロード
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

        # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            img = cv2.imdecode(img_array, 1)
            # グレースケール変換
            gray = rgb_to_gray(img)
            # 画像の保存

            cv2.imwrite(os.path.join(IMG_PATH + "gray.png"), gray)


    return render_template('index.html', images=os.path.join(IMG_PATH + "gray.png"))


if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)
