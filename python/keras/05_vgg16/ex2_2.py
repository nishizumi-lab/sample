# -*- coding: utf-8 -*-
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Dropout
from keras.optimizers import RMSprop
from keras.datasets import mnist
from keras.utils import np_utils, to_categorical
from keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import os

def main():
    # 入力画像のパラメータ
    img_width = 150 # 入力画像の幅
    img_height = 150 # 入力画像の高さ
    img_ch = 3 # 1ch画像（グレースケール）で学習

    # 入力データ数
    num_data = 1

    # データ格納用のディレクトリパス
    SAVE_DATA_DIR_PATH = "/Users/panzer5/github/sample/python/keras/05_vgg16/ex2_data/"

    # ラベル
    labels =['yakan', 'donabe', 'magcup']

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
    y_pred: [[9.8013526e-01 1.9847380e-02 1.7439326e-05]]
    number_pred: 0
    label_pred： yakan
    """

if __name__ == '__main__':
    main()
