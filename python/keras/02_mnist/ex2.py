# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import os
import pickle

def plot_history(history, 
                save_graph_img_path, 
                fig_size_width, 
                fig_size_height, 
                lim_font_size):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
   
    epochs = range(len(acc))

    # グラフ表示
    plt.figure(figsize=(fig_size_width, fig_size_height))
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = lim_font_size  # 全体のフォント
    #plt.subplot(121)

    # plot accuracy values
    plt.plot(epochs, acc, color = "blue", linestyle = "solid", label = 'train acc')
    plt.plot(epochs, val_acc, color = "green", linestyle = "solid", label= 'valid acc')
    #plt.title('Training and Validation acc')
    #plt.grid()
    #plt.legend()
 
    # plot loss values
    #plt.subplot(122)
    plt.plot(epochs, loss, color = "red", linestyle = "solid" ,label = 'train loss')
    plt.plot(epochs, val_loss, color = "orange", linestyle = "solid" , label= 'valid loss')
    #plt.title('Training and Validation loss')
    plt.legend()
    plt.grid()

    plt.savefig(save_graph_img_path)
    plt.close() # バッファ解放

def main():
    # ハイパーパラメータ
    batch_size = 128 # バッチサイズ
    num_classes = 10 # 分類クラス数(今回は0～9の手書き文字なので10)
    epochs = 20      # エポック数(学習の繰り返し回数)
    dropout_rate = 0.2 # 過学習防止用：入力の20%を0にする（破棄）
    num_middle_unit = 512 # 中間層のユニット数

    # 入力画像のパラメータ
    img_width = 28 # 入力画像の幅
    img_height = 28 # 入力画像の高さ

    # データの保存先(自分の環境に応じて適宜変更)
    SAVE_DATA_DIR_PATH = "C:/github/sample/python/keras/02_mnist/ex2_data/"

    # グラフ画像のサイズ
    FIG_SIZE_WIDTH = 12
    FIG_SIZE_HEIGHT = 10
    FIG_FONT_SIZE = 25

    # ディレクトリがなければ作成
    os.makedirs(SAVE_DATA_DIR_PATH, exist_ok=True)

    # 入力データ数（今回は28*28=784個）
    num_input = int(img_width * img_height)

    # データセット（訓練用データとテスト用データ）をネットから取得
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # 2次元配列から1次元配列へ変換（今回は28*28=784個の要素数）
    x_train = x_train.reshape(60000, num_input)
    x_test = x_test.reshape(10000, num_input)

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

    # 4層のMLP(多層パーセプトロン)のモデルを設定
    # 1層目の入力層:28×28=784個のユニット数
    # 2層目の中間層:ユニット数512、活性化関数はrelu関数
    model.add(Dense(activation='relu', input_dim=num_input, units=num_middle_unit))

    # ドロップアウト(過学習防止用, dropout_rate=0.2なら20%のユニットを無効化）
    model.add(Dropout(dropout_rate)) # 過学習防止用

    # 3層目の中間層:ユニット数512、活性化関数はrelu関数
    model.add(Dense(units=num_middle_unit, activation='relu'))

    # ドロップアウト(過学習防止用, dropout_rate=0.2なら20%のユニットを無効化）
    model.add(Dropout(dropout_rate))

    # 4層目の出力層:10分類（0から9まで）なので、ユニット数10, 分類問題なので活性化関数はsoftmax関数
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

    # テスト用データセットで学習済分類器に入力し、パフォーマンスを計測
    score = model.evaluate(x_test, 
                            y_test,
                            verbose=0
                            )

    # パフォーマンス計測の結果を表示
    # 損失値（値が小さいほど良い）
    print('Test loss:', score[0])

    # 正答率（値が大きいほど良い）
    print('Test accuracy:', score[1])
    
    # 学習過程をプロット
    plot_history(history, 
                save_graph_img_path = SAVE_DATA_DIR_PATH + "graph.png", 
                fig_size_width = FIG_SIZE_WIDTH, 
                fig_size_height = FIG_SIZE_HEIGHT, 
                lim_font_size = FIG_FONT_SIZE)

    # 学習履歴を保存
    with open(SAVE_DATA_DIR_PATH + "history.json", 'wb') as f:
        pickle.dump(history.history, f)

if __name__ == '__main__':
    main()