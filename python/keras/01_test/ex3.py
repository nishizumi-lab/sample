# -*- coding: utf-8 -*-
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense
from keras.optimizers import RMSprop
from keras.utils.vis_utils import plot_model

def main():

    SAVE_PLOT_MODEL_DIR_PATH = "/Users/panzer5/github/sample/python/keras/01_test/ex3_data/"
    # モデル構築
    model = Sequential()

    # 中間層(入力数:input_dim = 2, ユニット数:units = 3) 
    model.add(Dense(activation='sigmoid', input_dim=2, units=3))

    # 出力層(入力数:input_dim = 3だが、中間層のユニット数と同じなので省略可能, ユニット数:units = 2) 
    model.add(Dense(units=2, activation='sigmoid'))

    # 単純パーセプトロンをコンパイル（勾配法：RMSprop、損失関数：mean_squared_error、評価関数：accuracy）
    model.compile(loss='mean_squared_error', optimizer=RMSprop(), metrics=['accuracy'])

    # モデル構造の標準出力
    model.summary()

    # モデル構造の画像出力
    plot_model(model, to_file=SAVE_PLOT_MODEL_DIR_PATH + "plot_model.png")

if __name__ == '__main__':
    main()

    """
    on
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