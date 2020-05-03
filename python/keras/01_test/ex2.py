# -*- coding: utf-8 -*-
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense
from keras.optimizers import RMSprop

def main():
    # 説明変数（訓練用データ、入力データ）の用意
    train_x = np.array([[0.0, 0.0],
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [1.0, 1.0]])
    # 目的変数（正解データ）
    train_y = np.array([[0.0, 0.0],
                        [1.0, 0.0],
                        [1.0, 0.0],
                        [0.0, 0.0]])

    # モデル構築
    model = Sequential()

    # 中間層(入力数:input_dim = 2, ユニット数:units = 3) 
    model.add(Dense(activation='sigmoid', input_dim=2, units=3))

    # 出力層(入力数:input_dim = 3だが、中間層のユニット数と同じなので省略可能, ユニット数:units = 2) 
    model.add(Dense(units=2, activation='sigmoid'))

    # 単純パーセプトロンをコンパイル（勾配法：RMSprop、損失関数：mean_squared_error、評価関数：accuracy）
    model.compile(loss='mean_squared_error', optimizer=RMSprop(), metrics=['accuracy'])

    # 学習（教師データでフィッティング、バッチサイズ：4, エポック数：1000）
    history = model.fit(train_x, train_y, batch_size=4, epochs=3000)

    # 検証用データの用意
    test_x = train_x
    test_y = train_y
       
    # モデルの検証（性能評価）
    test_loss, test_acc = model.evaluate(train_x, train_y, verbose=0)
    print('test_loss:', test_loss) # 損失関数値（この値を最小化するようにパラメータ（重みやバイアス）の調整が行われる）
    print('test_acc:', test_acc) # 精度

    # 検証用データをモデルに入力し、出力（予測値）を取り出す
    predict_y = model.predict(test_x)
    print("test_y:", test_y)  # 正解データ
    print("predict_y:", predict_y)  # 予測データ

    # 出力値をしきい値処理
    threshold = 0.5
    print("thresholded predict_y:", (predict_y > threshold).astype(np.int))

    model.summary()

if __name__ == '__main__':
    main()

    """
    Epoch 3000/3000
    4/4 [==============================] - 0s 169us/step - loss: 0.0771 - accuracy: 1.0000
    test_loss: 0.07708477973937988
    test_acc: 1.0
    test_y: [[0. 0.]
    [1. 0.]
    [1. 0.]
    [0. 0.]]
    predict_y: [[1.4658220e-01 2.6109521e-04]
    [4.9374342e-01 7.2102230e-05]
    [8.1419665e-01 6.1752781e-04]
    [5.5170000e-01 7.7235760e-05]]
    thresholded predict_y: [[0 0]
    [0 0]
    [1 0]
    [1 0]]
    Model: "sequential_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    dense_1 (Dense)              (None, 3)                 9         
    _________________________________________________________________
    dense_2 (Dense)              (None, 2)                 8         
    =================================================================
    Total params: 17
    Trainable params: 17
    Non-trainable params: 0
    _________________________________________________________________
    """