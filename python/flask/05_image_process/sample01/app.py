from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import numpy as np
import cv2
from grayscale import rgb_to_gray


SAVE_DIR = "./images/"

if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")


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
            save_path = os.path.join(SAVE_DIR + "gray.png")
            cv2.imwrite(save_path, gray)


    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.debug = True  # デバッグモード有効化
    #app.run(host="0.0.0.0", port=port)
    app.run(host="127.0.0.1", port=port)
