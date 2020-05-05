# -*- coding: utf-8 -*-
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense
from keras.optimizers import RMSprop
import os

def main():

    # モデルの保存先
    SAVE_DATA_DIR_PATH = "/Users/panzer5/github/sample/python/keras/01_test/ex5_data/"
    
    # ディレクトリがなければ作成
    os.makedirs(SAVE_DATA_DIR_PATH, exist_ok=True)

    # 説明変数（訓練用データ、入力データ）の用意
    x_train = np.array([[0.0, 0.0],
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [1.0, 1.0]])
    # 目的変数（正解データ）
    y_train = np.array([[0.0, 0.0],
                        [1.0, 0.0],
                        [1.0, 0.0],
                        [0.0, 0.0]])

    # モデル構築
    model = Sequential()

    # 中間層(入力数:input_dim = 2, ユニット数:units = 3) 
    # Denseは全結合層のレイヤモジュール
    model.add(Dense(activation='sigmoid', input_dim=2, units=3))

    # 出力層(入力数:input_dim = 3だが、中間層のユニット数と同じなので省略可能, ユニット数:units = 2) 
    model.add(Dense(units=2, activation='sigmoid'))

    # 単純パーセプトロンをコンパイル（勾配法：RMSprop、損失関数：mean_squared_error、評価関数：accuracy）
    model.compile(loss='mean_squared_error', optimizer=RMSprop(), metrics=['accuracy'])

    # 学習（教師データでフィッティング、バッチサイズ：4, エポック数：1000）
    history = model.fit(x_train, y_train, batch_size=4, epochs=3000)

    # 検証用データの用意
    x_test = x_train
    y_test = y_train
       
    # モデル構造の保存
    open(SAVE_DATA_DIR_PATH  + "model.json","w").write(model.to_json())

    # 学習済みの重みを保存
    model.save_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # 保存したモデル構造の読み込み
    model2 = model_from_json(open(SAVE_DATA_DIR_PATH + "model.json", 'r').read())

    # 保存した学習済みの重みを読み込み
    model2.load_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # 検証用データの用意
    x_test = x_train
    y_test = y_train

   # 検証用データをモデルに入力し、出力（予測値）を取り出す
    predict_y = model2.predict(x_test)
    print("y_test:", y_test)  # 正解データ
    print("predict_y:", predict_y)  # 予測データ

    # 出力値をしきい値処理
    threshold = 0.5
    print("thresholded predict_y:", (predict_y > threshold).astype(np.int))

if __name__ == '__main__':
    main()

    """
    y_test: [[0. 0.]
    [1. 0.]
    [1. 0.]
    [0. 0.]]
    predict_y: [[1.2694235e-01 6.2597491e-04]
    [7.9402047e-01 6.8762962e-04]
    [5.1793259e-01 2.0202693e-04]
    [5.7249522e-01 2.1858796e-04]]
    thresholded predict_y: [[0 0]
    [1 0]
    [1 0]
    [1 0]]
    """