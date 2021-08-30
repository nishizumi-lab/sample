# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.datasets import mnist
from tensorflow.eras.utils import np_utils, to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import cv2
import os

def main():
    # 入力画像のパラメータ
    img_width = 32 # 入力画像の幅
    img_height = 32 # 入力画像の高さ
    img_ch = 3 # 3ch画像（RGB）で学習

    # 入力データ数
    num_data = 1

    # データ格納用のディレクトリパス
    SAVE_DATA_DIR_PATH = "C:/github/sample/python/keras/03_cifar10/ex1_data/"

    # ラベル
    labels =['飛行機', '自動車', '鳥', '猫', '鹿', '犬', '蛙', '馬', '船', 'トラック']

    # 保存したモデル構造の読み込み
    model = model_from_json(open(SAVE_DATA_DIR_PATH + "model.json", 'r').read())

    # 保存した学習済みの重みを読み込み
    model.load_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # 画像の読み込み（32×32にリサイズ）
    # 正規化, 4次元配列に変換（モデルの入力が4次元なので合わせる）
    img = load_img(SAVE_DATA_DIR_PATH + "test.png", target_size=(img_width, img_height))
    img = img_to_array(img) 
    img = img.astype('float32')/255.0
    img = np.array([img])

    # 分類機に入力データを与えて予測（出力：各クラスの予想確率）
    y_pred = model.predict(img)

    # 最も確率の高い要素番号（=予想する数字）
    number_pred = np.argmax(y_pred) 

    # 予測結果の表示
    print("y_pred:", y_pred)  # 出力値
    print("number_pred:", number_pred)  # 最も確率の高い要素番号
    print('label_pred：', labels[int(number_pred)]) # 予想ラベル（最も確率の高い要素）

    """
    y_pred: [[1.05510656e-10 9.90023911e-01 7.12201237e-16 6.99716381e-17
    9.21270893e-22 1.03125948e-20 5.56179723e-13 2.53434248e-15
    1.68777863e-08 9.97608900e-03]]
    number_pred: 1
    label_pred： 自動車
    """

if __name__ == '__main__':
    main()
