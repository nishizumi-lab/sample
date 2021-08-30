# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import np_utils, to_categorical
import matplotlib.pyplot as plt
import cv2
import os

def main():
    # 入力画像のパラメータ
    img_width = 28 # 入力画像の幅
    img_height = 28 # 入力画像の高さ
    img_ch = 1 # 1ch画像（グレースケール）で学習

    # 入力データ数
    num_data = 1

    # データ格納用のディレクトリパス
    SAVE_DATA_DIR_PATH = "C:/github/sample/python/keras/02_mnist/ex3_data/"

    # 保存したモデル構造の読み込み
    model = model_from_json(open(SAVE_DATA_DIR_PATH + "model.json", 'r').read())

    # 保存した学習済みの重みを読み込み
    model.load_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # カメラ画像の整形
    img = cv2.imread(SAVE_DATA_DIR_PATH + "test.png")

    # グレースケールに変換
    # 2値化, 白黒反転, ガウシアンフィルタで平滑化、リサイズ
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) # 
    th = cv2.bitwise_not(th) # 
    th = cv2.GaussianBlur(th, (9,9), 0) # 
    th = cv2.resize(th,(img_width, img_height), cv2.INTER_CUBIC) # 訓練データと同じサイズに整形

    # float32に変換して正規化
    th = th.astype('float32')
    th = np.array(th)/255

    # モデルの入力次元数に合わせてリサイズ
    th = th.reshape(num_data, img_height, img_width, img_ch)

    # 分類機に入力データを与えて予測（出力：各クラスの予想確率）
    predict_y = model.predict(th)

    # 最も確率の高い要素番号（=予想する数字）
    predict_number = np.argmax(predict_y) 

    # 予測結果の表示
    print("predict_y:", predict_y)  # 出力値
    print("predict_number:", predict_number)  # 予測した数字

    # 分類機に入力データを与えて予測（出力：クラスラベル）
    predict_classes_y = model.predict_classes(th)
    print("predict_classes_y:", predict_classes_y)  # 予測した数字

    """
    predict_y: [[2.0631208e-16 8.2029376e-11 1.0000000e+00 8.4496722e-13 4.3476162e-22
    4.4720264e-21 3.8950523e-22 5.1041643e-18 1.4993143e-12 1.6509382e-13]]
    predict_number: 2
    predict_classes_y: [2]
    """

if __name__ == '__main__':
    main()