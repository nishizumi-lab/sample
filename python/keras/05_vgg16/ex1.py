# -*- coding: utf-8 -*-
import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image

def main():
    # データ格納用のディレクトリパス
    SAVE_DATA_DIR_PATH = "C:/github/sample/python/keras/05_vgg16/ex1_data/"

    # VGG16の学習済みモデルを読み込み
    model = VGG16(weights='imagenet')

    # 入力画像の読み込み（VGG16の標準サイズ(224x224)にリサイズ）
    img = image.load_img(SAVE_DATA_DIR_PATH + "test.png", target_size=(224, 224))

    # NumPy配列に変換
    x = image.img_to_array(img)

    # 3次元配列→4次元配列
    x = np.expand_dims(x, axis=0)

    # 予測
    preds = model.predict(preprocess_input(x))

    # 予測結果（第1～5候補）の表示
    results = decode_predictions(preds, top=5)[0] # 出力ベクトルを文字列に変換
    for result in results:
        print(result)

    """
    ('n04037443', 'racer', 0.7069848)
    ('n04285008', 'sports_car', 0.12393004)
    ('n02974003', 'car_wheel', 0.08807774)
    ('n03770679', 'minivan', 0.013199047)
    ('n02814533', 'beach_wagon', 0.011577174)
    """ 

if __name__ == '__main__':
    main()