# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import np_utils, to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import cv2
import os

def main():
    # 入力画像のパラメータ
    img_width = 32 # 入力画像の幅
    img_height = 32 # 入力画像の高さ
    img_ch = 3 # 3ch画像（RGB）

    # 入力データ数
    num_data = 1

    # データ格納用のディレクトリパス
    SAVE_DATA_DIR_PATH = "C:/github/sample/python/keras/04_img/ex1_data/"

    # ラベル
    labels =['やかん', '土鍋', 'マグカップ']

    # 保存したモデル構造の読み込み
    model = model_from_json(open(SAVE_DATA_DIR_PATH + "model.json", 'r').read())

    # 保存した学習済みの重みを読み込み
    model.load_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # 画像の読み込み（32×32にリサイズ）
    # 正規化, 4次元配列に変換（モデルの入力が4次元なので合わせる）
    img = load_img(SAVE_DATA_DIR_PATH + "test.jpg", target_size=(img_width, img_height))
    img = img_to_array(img) 
    img = img.astype('float32')/255.0
    img = np.array([img])

    # 分類機に入力データを与えて予測（出力：各クラスの予想確率）
    y_pred = model.predict(img)

    # 最も確率の高い要素番号
    number_pred = np.argmax(y_pred) 

    # 予測結果の表示
    print("y_pred:", y_pred)  # 出力値
    print("number_pred:", number_pred)  # 最も確率の高い要素番号
    print('label_pred：', labels[int(number_pred)]) # 予想ラベル（最も確率の高い要素）


    """
    predict_y: [[1.2638741e-20 4.6908645e-21 1.0000000e+00]]
    predict_number: 2
    predict_label： マグカップ
    """

if __name__ == '__main__':
    main()
