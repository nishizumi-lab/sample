# -*- coding: utf-8 -*-
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Dropout
from keras.optimizers import RMSprop
from keras.datasets import mnist
from keras.utils import np_utils, to_categorical
from keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import cv2
import os

def main():
    # 入力画像のパラメータ
    img_width = 32 # 入力画像の幅
    img_height = 32 # 入力画像の高さ
    img_ch = 1 # 1ch画像（グレースケール）で学習

    # 入力データ数
    num_data = 1

    # データ格納用のディレクトリパス
    SAVE_DATA_DIR_PATH = "/Users/panzer5/github/sample/python/keras/03_cifar10/ex1_data/"

    # ラベル
    labels =['飛行機', '自動車', '鳥', '猫', '鹿', '犬', '蛙', '馬', '船', 'トラック']

    # 保存したモデル構造の読み込み
    model = model_from_json(open(SAVE_DATA_DIR_PATH + "model.json", 'r').read())

    # 保存した学習済みの重みを読み込み
    model.load_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # 画像の読み込み（32×32にリサイズ）
    # 正規化, 4次元配列に変換（モデルの入力が4次元なので合わせる）
    img = load_img("input.jpg", target_size=(32, 32))
    img = img_to_array(img) 
    img = img.astype('float32')/255.0
    img = np.array([img])

    # 分類機に入力データを与えて予測（出力：各クラスの予想確率）
    y_pred = model.predict(img)

    # 最も確率の高い要素番号（=予想する数字）
    number_pred = np.argmax(y_pred) 

    # 予測結果の表示
    print("predict_y:", y_pred)  # 出力値
    print("predict_number:", number_pred)  # 最も確率の高い要素番号
    print('predict_label：', labels[int(number_pred)]) # 予想ラベル（最も確率の高い要素）



    """
    predict_y: [[2.0631208e-16 8.2029376e-11 1.0000000e+00 8.4496722e-13 4.3476162e-22
    4.4720264e-21 3.8950523e-22 5.1041643e-18 1.4993143e-12 1.6509382e-13]]
    predict_number: 2
    predict_classes_y: [2]
    """

if __name__ == '__main__':
    main()