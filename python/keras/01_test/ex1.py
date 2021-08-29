# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import RMSprop

def main():
    # 説明変数（訓練用データ、入力データ）の用意
    x_train = np.array([[0.0, 0.0],
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [1.0, 1.0]])
    # 目的変数（正解データ）
    y_train = np.array([[0.0, 0.0],
                        [0.0, 0.0],
                        [0.0, 0.0],
                        [1.0, 0.0]])

    # モデル生成
    model = Sequential()

    # 中間層(入力数:input_dim = 2, ユニット数:units = 3) 
    # Denseは全結合層のレイヤモジュール
    model.add(Dense(activation='sigmoid', input_dim=2, units=3))

    # 出力層(入力数:input_dim = 3だが、中間層のユニット数と同じなので省略可能, 出力数:units = 2) 
    model.add(Dense(units=2, activation='sigmoid'))

    # 単純パーセプトロンをコンパイル（勾配法：RMSprop、損失関数：mean_squared_error、評価関数：accuracy）
    model.compile(loss='mean_squared_error', optimizer=RMSprop(), metrics=['accuracy'])

    # 学習（教師データでフィッティング、バッチサイズ：4, エポック数：1000）
    history = model.fit(x_train, y_train, batch_size=4, epochs=3000)

    # 検証用データの用意
    x_test = x_train
    y_test = y_train
       
    # モデルの検証（性能評価）
    test_loss, test_acc = model.evaluate(x_train, y_train, verbose=0)
    print('test_loss:', test_loss) # 損失関数値（この値を最小化するようにパラメータ（重みやバイアス）の調整が行われる）
    print('test_acc:', test_acc) # 精度

    # 検証用データをモデルに入力し、出力（予測値）を取り出す
    predict_y = model.predict(x_test)
    print("y_test:", y_test)  # 正解データ
    print("predict_y:", predict_y)  # 予測データ

    # 出力値をしきい値処理
    threshold = 0.5
    print("thresholded predict_y:", (predict_y > threshold).astype(np.int))


if __name__ == '__main__':
    main()

    """
    Epoch 2999/3000
    4/4 [==============================] - 0s 158us/step - loss: 0.0059 - accuracy: 1.0000
    Epoch 3000/3000
    4/4 [==============================] - 0s 163us/step - loss: 0.0059 - accuracy: 1.0000
    test_loss: 0.005894103087484837

    test_acc: 1.0

    y_test: [
    [0. 0.]
    [0. 0.]
    [0. 0.]
    [1. 0.]]

    predict_y: [
    [4.8003150e-03 3.0511411e-04]
    [1.0174283e-01 1.7523641e-03]
    [1.1211305e-01 1.4651634e-04]
    [8.4442729e-01 1.6705699e-03]]

    thresholded predict_y: [
    [0 0]
    [0 0]
    [0 0]
    [1 0]]
    """
