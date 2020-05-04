# -*- coding: utf-8 -*-
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Dropout
from keras.optimizers import RMSprop
from keras.datasets import mnist
from keras.utils import np_utils, to_categorical
import os

def main():
    # パラメータ
    batch_size = 128 # バッチサイズ(データサイズ)
    num_classes = 10 # 分類クラス数(今回は0～9の手書き文字なので10)
    epochs = 20 # エポック数(学習の繰り返し回数)

    # mnistデータセット（訓練用データと検証用データ）をネットから取得
    (train_x, train_y), (test_x, test_y) = mnist.load_data()

    # 2次元配列から1次元配列へ変換（28*28=784次元のベクトル）
    train_x = train_x.reshape(60000, 28*28)
    test_x = test_x.reshape(10000, 28*28)

    # データ型をfloat32に変換
    train_x = train_x.astype('float32')
    test_x = test_x.astype('float32')

    # 正規化(0-255から0.0-1.0に変換）
    train_x /= 255
    test_x /= 255

    # カテゴリー変数を学習しやすいよう, 0と1で表現する処理(one-hot encodings)
    train_y = to_categorical(train_y, num_classes)
    test_y = to_categorical(test_y, num_classes)

    # 検証用最後の5000個のトレーニングサンプルを分割
    train_x, valid_x = np.split(train_x, [55000])
    train_y, valid_y = np.split(train_y, [55000])

    # データセットの個数を表示
    print(train_x.shape[0], 'train samples')
    print(test_x.shape[0], 'test samples')

    # モデルの構築
    model = Sequential()

    # Dense：全結合のニューラルネットワークレイヤー
    # 入力層784次元(=28x28)、出力層512次元
    model.add(Dense(512, activation='relu', input_shape=(784,)))
    model.add(Dropout(0.2)) # 過学習防止用：入力の20%を0にする（破棄）
    model.add(Dense(512, activation='relu')) # 活性化関数：relu
    model.add(Dropout(0.2)) # 過学習防止用：入力の20%を0にする（破棄）
    model.add(Dense(num_classes, activation='softmax')) # 活性化関数：softmax
    model.summary()

    # コンパイル（多クラス分類問題）
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])

    # 構築したモデルで学習
    history = model.fit(train_x, 
                        train_y, 
                        batch_size=batch_size, 
                        epochs=epochs, 
                        verbose=1, 
                        validation_data=(valid_x, valid_y))

    score = model.evaluate(test_x, 
                            test_y,
                            verbose=0
                            )

    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    
    """
    Test score: 0.1320522134795261
    Test accuracy: 0.9837999939918518
    """

if __name__ == '__main__':
    main()