# -*- coding: utf-8 -*-
import numpy as np
import os
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras import optimizers
import pickle
import matplotlib.pyplot as plt

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

def build_model(num_classes=3,                 
                img_width=32, 
                img_height=32):
    # VGG16の読み込み（FC層は不要なので include_topはFalse）
    input_tensor = Input(shape=(img_width, img_height, 3))
    vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

    # FC層の作成
    model = Sequential()
    model.add(Flatten(input_shape=vgg16.output_shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    # VGG16とFC層を結合してモデルを作成
    new_model = Model(input = vgg16.input, output=model(vgg16.output))

    return new_model



# 訓練用データ（画像）と検証用データ（画像）をロード
def img_generator(classes, 
                train_path, 
                validation_path, 
                batch_size=16, 
                img_width=32, 
                img_height=32):

    # ディレクトリ内の画像を読み込んでトレーニングデータとバリデーションデータの作成
    train_gen = ImageDataGenerator(rescale=1.0 / 255, zoom_range=0.2, horizontal_flip=True)

    validation_gen = ImageDataGenerator(rescale=1.0 / 255)

    tg = train_gen.flow_from_directory(train_path,
        target_size=(img_width, img_height),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True)

    vg = validation_gen.flow_from_directory(
        validation_path,
        target_size=(img_width, img_height),
        color_mode='rgb',
        classes=classes,
        class_mode='categorical',
        batch_size=batch_size,
        shuffle=True)

    return tg, vg


def main():
    num_epoch = 10
    samples_per_epoch = 100


    nb_val_samples = 50

    # バッチサイズ
    batch_size = 16

    # 画像の高さ, 幅
    img_width = 150
    img_height = 150
    # クラス数
    num_classes = 3
    # 分類するクラス名
    classes = ['yakan', 'donabe', 'mag']

    # グラフ画像のサイズ
    FIG_SIZE_WIDTH = 12
    FIG_SIZE_HEIGHT = 10
    FIG_FONT_SIZE = 25

    # トレーニング用とバリデーション用の画像格納先
    SAVE_DATA_DIR_PATH = '/Users/panzer5/github/sample/python/keras/05_vgg16/ex2_data/'

    # ディレクトリがなければ作成
    os.makedirs(SAVE_DATA_DIR_PATH, exist_ok=True)

    # モデル作成
    model = build_model(num_classes = num_classes, 
                        img_width = img_width,
                        img_height = img_height)

    # 最後のconv層の直前までの層をfreeze
    for layer in model.layers[:15]:
        layer.trainable = False

    # 多クラス分類を指定
    model.compile(loss = 'categorical_crossentropy',
              optimizer = optimizers.SGD(lr=1e-3, momentum=0.9),
              metrics=['accuracy'])

    # 画像のジェネレータ生成
    train_datas, valid_datas = img_generator(classes = classes,
                            train_path = SAVE_DATA_DIR_PATH + "train/", 
                            validation_path = SAVE_DATA_DIR_PATH + "validation/",
                            batch_size = batch_size,
                            img_width = img_width,
                            img_height = img_height)

    # Fine-tuning
    history = model.fit_generator(train_datas,
        samples_per_epoch = samples_per_epoch,
        nb_epoch = num_epoch,
        validation_data = valid_datas,
        nb_val_samples = nb_val_samples)

 
    # モデル構造の保存
    open(SAVE_DATA_DIR_PATH  + "model.json","w").write(model.to_json())  

    # 学習済みの重みを保存
    model.save_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # 学習履歴を保存
    with open(SAVE_DATA_DIR_PATH + "history.json", 'wb') as f:
        pickle.dump(history.history, f)

    # 学習過程をプロット
    plot_history(history, 
                save_graph_img_path = SAVE_DATA_DIR_PATH + "graph.png", 
                fig_size_width = FIG_SIZE_WIDTH, 
                fig_size_height = FIG_SIZE_HEIGHT, 
                lim_font_size = FIG_FONT_SIZE)

if __name__ == '__main__':
    main()