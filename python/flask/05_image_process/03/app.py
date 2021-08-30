from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import cv2
import os
from datetime import datetime as dt

app = Flask(__name__, static_url_path="")

BASE_DIR = os.path.dirname(__file__)

# 処理した画像ファイルの保存先
IMG_DIR = "/static/images/"
MODEL_DIR = "/static/models/"

# 分類に使う学習済ファイルの保存先
IMG_PATH = BASE_DIR + IMG_DIR
MODEL_PATH = BASE_DIR + MODEL_DIR


@app.route('/', methods=['GET', 'POST'])
def index():
    img_name = ""
    img_label = ""

    # 入力画像のパラメータ
    img_width = 224 # 入力画像の幅
    img_height = 224 # 入力画像の高さ

    # ラベル
    labels =['やかん', '土鍋', 'マグカップ']



    if request.method == 'POST':
        # 画像をロード
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)


        # 画像データ用配列にデータがあれば
        if len(img_array) != 0:
            # 画像のリサイズ
            img = cv2.imdecode(img_array, 1)
            #img = cv2.resize(img, dsize=(img_width, img_height))
            # リサイズした画像の保存
            now_date = dt.now()
            img_name = "img" + now_date.strftime('%Y-%m-%d-%H-%M-%S') + ".jpg"
            cv2.imwrite(os.path.join(IMG_PATH + img_name), img)
            
            # 画像の読み込み（32×32にリサイズ）
            # 正規化, 4次元配列に変換（モデルの入力が4次元なので合わせる）
            img = load_img(IMG_PATH + img_name, target_size=(img_width, img_height))
            img = img_to_array(img) 
            img = img.astype('float32')/255.0
            img = np.array([img])
            print(img.shape)
            print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJ")

            # 保存したモデル構造の読み込み
            model = model_from_json(open(MODEL_PATH + "model.json", 'r').read())

            # 保存した学習済みの重みを読み込み
            model.load_weights(MODEL_PATH + "weight.hdf5")
            # 分類機に入力データを与えて予測（出力：各クラスの予想確率）
            y_pred = model.predict(img)

            # 最も確率の高い要素番号
            number_pred = np.argmax(y_pred) 

            # 予測結果の表示
            print("y_pred:", y_pred)  # 出力値
            print("number_pred:", number_pred)  # 最も確率の高い要素番号
            print('label_pred：', labels[int(number_pred)]) # 予想ラベル（最も確率の高い要素）

            img_label = labels[int(number_pred)]

    return render_template('index.html', img_name=img_name, img_label=img_label)


if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)
