# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import svm
import joblib
import matplotlib.pyplot as plt
from sklearn import metrics 
from sklearn import datasets  # データセットのロード用
from sklearn.model_selection import train_test_split # データセットの分割用
import cv2

class SVM():
    # 学習
    def train(self,
        save_trained_data_path,
        train_X,
        train_y,
        gamma,
        C,
        kernel):

        # 学習（SVM）
        clf = svm.SVC(gamma=gamma, C=C, kernel=kernel)
        clf.fit(train_X, train_y)
        joblib.dump(clf, save_trained_data_path)

    # 検証
    def test(self,
        load_trained_data_path,
        test_X,
        test_y):

        # 学習済ファイルのロード
        clf = joblib.load(load_trained_data_path)

        # 学習結果の検証（テスト用データx1, x2を入力）
        predicted_y = clf.predict(test_X)

        # 正解データと予測データを比較し、スコアを計算
        score = metrics.accuracy_score(test_y, predicted_y)

        # 検証結果の表示
        print("Score：", score)

    # 予測
    def predict(self,
        load_trained_data_path,
        test_X):
        # 学習済ファイルのロード
        clf = joblib.load(load_trained_data_path)

        # モデルに入力し、予測値を計算
        predicted_y = clf.predict(test_X)
        
        return predicted_y

def main():
    # 学習済みモデルデータの出力先パス
    SAVE_TRAINED_DATA_PATH = 'C:/github/sample/python/scikit/svm/ex6_data/train.learn'

    # テスト用の画像データ（ペイントソフトで2と書いて保存したもの）
    LOAD_TEST_IMG_PATH = 'C:/github/sample/python/scikit/svm/ex6_data/test_2.png'

    # SVMのパラメータ
    GAMMA = 0.1
    C = 1
    KERNEL = "linear" # 手書き数字画像の場合はrbfだと学習結果が悪い

    # クラスのデータとプロット時に割り当てる色
    CLASS_DATAS = [0, 1, 2]
    CLASS_COLORS = ["blue", "red", "green"]

    svm = SVM()

    # 学習用のデータを読み込み(Irisデータセットを利用)
    digits_dataset = datasets.load_digits()

    # 説明変数（学習データ：手書き数字の画像データ8*8, 2次元配列）を抽出
    X = digits_dataset.images

    print("X1:", X[1])
    
    # 目的変数：数字（0～9）
    y = digits_dataset.target
    
    # xの二次元配列を１次元に変換(-1で変換元の要素数に合わせて自動で値が決定：変換前要素数=変換後要素数となる）
    X = X.reshape((-1, 64))
    
    # 説明変数のデータを、学習用データと検証用データに分割(学習用90%、検証用10％、シャッフルする)
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, shuffle=True)
    print("train_X size:", train_X.shape)
    print("train_y size:", train_y.shape)
    print("test_X size:", test_X.shape)
    print("test_y size:", test_y.shape)

    # 学習済みモデルの作成
    svm.train(save_trained_data_path = SAVE_TRAINED_DATA_PATH,
            train_X=train_X,
            train_y=train_y,
            gamma = GAMMA,
            C = C,
            kernel = KERNEL)

    # 学習済みモデルの検証
    svm.test(
        load_trained_data_path = SAVE_TRAINED_DATA_PATH,
        test_X=test_X,
        test_y=test_y)

    # 学習済みモデルを使って予測

    # OpenCVで任意の手書き数字画像をロードし,
    # グレースケール変換, 、白黒反転
    # 8*8にリサイズ, 1次元配列に変換,
    # 値を0～16に収めてモデルに入力
    test_img = cv2.imread(LOAD_TEST_IMG_PATH)
    test_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    test_gray = cv2.bitwise_not(test_gray)
    test_gray = cv2.resize(test_gray, (8, 8))
    test_gray = test_gray.reshape(-1, 64)
    test_gray = np.clip(test_gray, 0, 16)

    predict_y = svm.predict(
        load_trained_data_path = SAVE_TRAINED_DATA_PATH,
        test_X=test_gray)

    print("test_X:", test_gray)
    print("predict_y:", predict_y)



    """
    X1: [[ 0.  0.  0. 12. 13.  5.  0.  0.]
    [ 0.  0.  0. 11. 16.  9.  0.  0.]
    [ 0.  0.  3. 15. 16.  6.  0.  0.]
    [ 0.  7. 15. 16. 16.  2.  0.  0.]
    [ 0.  0.  1. 16. 16.  3.  0.  0.]
    [ 0.  0.  1. 16. 16.  6.  0.  0.]
    [ 0.  0.  1. 16. 16.  6.  0.  0.]
    [ 0.  0.  0. 11. 16. 10.  0.  0.]]

    train_X size: (1437, 64)
    train_y size: (1437,)
    test_X size: (360, 64)
    test_y size: (360,)

    Score： 0.9805555555555555

    test_X: [[ 0  0  0  0  0  0  0  0  0  0 16 16  0  0  0  0  0  0  0  0 16  0  0  0
    0  0  0  0 16  0  0  0  0  0  0  0 16  0  0  0  0  0 16  0  0  0  0  0
    0  0 16 16 16 16  0  0  0  0  0  0  0  0  0  0]]

    predict_y: [2]

    """

if __name__ == "__main__":
    main()
