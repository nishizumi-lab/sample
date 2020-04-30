# -*- coding: utf-8 -*-
from keras.utils import plot_model
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
from keras.utils import plot_model

def main():
    # 説明変数（訓練用データ、入力データ）の用意
    train_x = np.array([[0.0, 0.0],
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [1.0, 1.0]])
    # 目的変数（正解データ）
    train_y = np.array([0.0, 1.0, 1.0, 0.0])

    # モデル構築
    model = Sequential()

    # 中間層(入力数:input_dim = 2, 出力数:units = 2) 
    model.add(Dense(activation='sigmoid', input_dim=2, units=2))

    # 出力層(入力数:input_dim = 2だが、中間層の出力数と同じなので省略可能, 出力数:units = 1) 
    model.add(Dense(units=1, activation='sigmoid'))

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


    plot_model(model, to_file='model.png')

    # Plot training & validation accuracy values
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()
if __name__ == '__main__':
    main()

    """
    test_loss: 0.23982135951519012
    test_acc: 0.75
    test_y: [0. 1. 1. 0.]
    predict_y: [[0.46847287]
    [0.5179871 ]
    [0.50366074]
    [0.5110083 ]]
    thresholded predict_y: [[0]
    [1]
    [1]
    [1]]
    Model: "sequential_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    dense_1 (Dense)              (None, 2)                 6         
    _________________________________________________________________
    dense_2 (Dense)              (None, 1)                 3         
    =================================================================
    Total params: 9
    Trainable params: 9
    Non-trainable params: 0
    _________________________________________________________________
    """
