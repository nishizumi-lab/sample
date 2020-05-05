# -*- coding: utf-8 -*-
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense
from keras.optimizers import RMSprop
import os
import pickle
import matplotlib.pyplot as plt

def plot_history(history, save_graph_img_path, fig_size_x, fig_size_y, lim_font_size):


    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
   
    epochs = range(len(acc))

    # グラフ表示
    plt.figure(figsize=(fig_size_x, fig_size_y))
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = lim_font_size  # 全体のフォント
    plt.subplot(121)

    plt.plot(epochs, acc, 'bo' ,label = 'training acc')
    plt.plot(epochs, val_acc, 'b' , label= 'validation acc')
    plt.title('Training and Validation acc')
    plt.grid()
    plt.legend()

 
    plt.subplot(122)
    plt.plot(epochs, loss, 'bo' ,label = 'training loss')
    plt.plot(epochs, val_loss, 'b' , label= 'validation loss')
    plt.title('Training and Validation loss')
    plt.legend()
    plt.grid()

    plt.savefig(save_graph_img_path)
    plt.close() # バッファ解放

def main():

    SAVE_DATA_DIR_PATH = "/Users/panzer5/github/sample/python/keras/01_test/ex4_data/"
    
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

    # 検証用データ
    x_test = x_train
    y_test = y_train

    # モデル構築
    model = Sequential()

    # 中間層(入力数:input_dim = 2, ユニット数:units = 3) 
    model.add(Dense(activation='sigmoid', input_dim=2, units=3))

    # 出力層(入力数:input_dim = 3だが、中間層のユニット数と同じなので省略可能, ユニット数:units = 2) 
    model.add(Dense(units=2, activation='sigmoid'))

    # 単純パーセプトロンをコンパイル（勾配法：RMSprop、損失関数：mean_squared_error、評価関数：accuracy）
    model.compile(loss='mean_squared_error', optimizer=RMSprop(), metrics=['accuracy'])

    # 学習（教師データでフィッティング、バッチサイズ：4, エポック数：3000）
    history = model.fit(
                        x_train, 
                        y_train, 
                        batch_size=4, 
                        epochs=3000,
                        validation_data=(x_test, y_test)) # 検証用データ

    plot_history(history, SAVE_DATA_DIR_PATH + "graph.png", 25, 10, 25)

    # 学習履歴を保存
    with open(SAVE_DATA_DIR_PATH + "history.json", 'wb') as f:
        pickle.dump(history.history, f)

if __name__ == '__main__':
    main()


