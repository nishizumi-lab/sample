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

# 減色処理
def sub_color(src, K):
    # 次元数を1落とす
    Z = src.reshape((-1,3))

    # float32型に変換
    Z = np.float32(Z)

    # 基準の定義
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # K-means法で減色
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # UINT8に変換
    center = np.uint8(center)

    res = center[label.flatten()]

    # 配列の次元数と入力画像と同じに戻す
    return res.reshape((src.shape))


# モザイク処理
def mosaic(img, alpha):
    # 画像の高さ、幅、チャンネル数
    h, w, ch = img.shape

    # 縮小→拡大でモザイク加工
    img = cv2.resize(img,(int(w*alpha), int(h*alpha)))
    img = cv2.resize(img,(w, h), interpolation=cv2.INTER_NEAREST)

    return img


# ドット絵化
def pixel_art(img, alpha=2, K=4):
    # モザイク処理
    img = mosaic(img, alpha)

    # 減色処理
    return sub_color(img, K)


@app.route('/', methods=['GET', 'POST'])
def index():
    img_name = ""

    if request.method == 'POST':
        # 画像処理のパラメータを取得
        alpha = float(request.form['alpha'])
        K = int(request.form['K'])

        # POSTで画像データを受信
        stream = request.files['image'].stream

        # NumPy配列に変換し、OpenCVで扱えるようにする
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

        # 画像データ用配列にデータがあれば処理
        if len(img_array) != 0:
            # デコード
            img = cv2.imdecode(img_array, 1)
            # モザイクアート加工
            dst = pixel_art(img, alpha, K)

            # 出力ファイル名の生成(現在日時を付与して被らないようにする)
            now_date = dt.now()
            img_name = "dst-" + now_date.strftime('%Y-%m-%d-%H-%M-%S') + ".png"
            
            # 画像の保存
            cv2.imwrite(os.path.join(IMG_PATH + img_name), dst)


    return render_template('index.html', img_name=img_name)


if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)
