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
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # 2次元配列から1次元配列へ変換（28*28=784次元のベクトル）
    x_train = x_train.reshape(60000, 28*28)
    x_test = x_test.reshape(10000, 28*28)

    # データ型をfloat32に変換
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    # 正規化(0-255から0.0-1.0に変換）
    x_train /= 255
    x_test /= 255

    # カテゴリー変数を学習しやすいよう, 0と1で表現する処理(one-hot encodings)
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    # データセットの個数を表示
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

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

    # 構築したモデルで学習（学習データ:trainのうち、10％を検証データ:validationとして使用）
    history = model.fit(x_train, 
                        y_train, 
                        batch_size=batch_size, 
                        epochs=epochs, 
                        verbose=1, 
                        validation_split=0.1)

    score = model.evaluate(x_test, 
                            y_test,
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