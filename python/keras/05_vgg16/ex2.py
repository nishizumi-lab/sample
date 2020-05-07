# -*- coding: utf-8 -*-
import numpy as np
import os
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dropout, Flatten, Dense
from keras import optimizers
import pickle

def build_model(nb_classes=5, width=150, height=150):
    # VGG16の読み込み（FC層は不要なので include_topはFalse）
    input_tensor = Input(shape=(width, height, 3))
    vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

    # FC層の作成
    model = Sequential()
    model.add(Flatten(input_shape=vgg16.output_shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation='softmax'))

    # VGG16とFC層を結合してモデルを作成
    new_model = Model(input = vgg16.input, output=model(vgg16.output))

    return new_model



# 画像の生成
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

    return (tg, vg)


def main():
    nb_epoch = 10
    nb_train_samples = 200
    nb_validation_samples = 50
    batch_size = 16
    img_width = 32
    img_height = 32
    # 分類するクラス
    classes = ['yakan', 'donabe', 'mag']
    # トレーニング用とバリデーション用の画像格納先
    SAVE_DATA_DIR_PATH = '/Users/panzer5/github/sample/python/keras/05_vgg16/ex2_data/'

    # モデル作成
    model = build_model()

    # 最後のconv層の直前までの層をfreeze
    for layer in model.layers[:15]:
        layer.trainable = False

    # 多クラス分類を指定
    model.compile(loss = 'categorical_crossentropy',
              optimizer = optimizers.SGD(lr=1e-3, momentum=0.9),
              metrics=['accuracy'])

    # 画像のジェネレータ生成
    tg, vg = img_generator(classes = classes,
                            train_path = SAVE_DATA_DIR_PATH + "train/", 
                            validation_path = SAVE_DATA_DIR_PATH + "validation/",
                            batch_size = batch_size,
                            img_width = img_width,
                            img_height = img_height)

    # Fine-tuning
    history = model.fit_generator(tg,
        samples_per_epoch = nb_train_samples,
        nb_epoch = nb_epoch,
        validation_data = vg,
        nb_val_samples = nb_validation_samples)

 
    # モデル構造の保存
    open(SAVE_DATA_DIR_PATH  + "model.json","w").write(model.to_json())  

    # 学習済みの重みを保存
    model.save_weights(SAVE_DATA_DIR_PATH + "weight.hdf5")

    # 学習履歴を保存
    with open(SAVE_DATA_DIR_PATH + "history.json", 'wb') as f:
        pickle.dump(history.history, f)

if __name__ == '__main__':
    main()