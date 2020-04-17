# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import svm
import joblib
import matplotlib.pyplot as plt
from sklearn import metrics 
from sklearn.datasets import load_iris # データセットのロード用
from sklearn.model_selection import train_test_split # データセットの分割用

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

    # 決定境界のプロット
    def plot2d(self,
        load_trained_data_path,
        save_graph_img_path,
        train_X,
        train_y,
        class_datas, 
        class_colors,
        x1_name,
        x2_name,
        x1_0 = None,
        x1_n = None,
        x2_0 = None,
        x2_n = None,
        fig_size_x = 10,
        fig_size_y = 10,
        N_x1=100,
        N_x2=100,
        lim_font_size = 22,   
    ):

        # 学習済ファイルのロード
        clf = joblib.load(load_trained_data_path)

        # 学習用データの説明変数の最大値、最小値を計算
        x1_min = train_X.T[0].min()
        x1_max = train_X.T[0].max()
        x2_min = train_X.T[1].min()
        x2_max = train_X.T[1].max()

        # 説明変数の最大値、最小値から格子データの範囲を計算
        if x1_0 == None:
            x1_0 = x1_min - 0.1 * (x1_max - x1_min)
        if x1_n == None:
            x1_n = x1_max + 0.1 * (x1_max - x1_min)

        if x2_0 == None:
            x2_0 = x2_min - 0.1 * (x2_max - x2_min)

        if x2_n == None:
            x2_n = x2_max + 0.1 * (x2_max - x2_min)

        # 境界線プロット用の格子状データを生成
        x1 = np.linspace(x1_0, x1_n, N_x1)
        x2 = np.linspace(x2_0, x2_n, N_x2)
        
        X1, X2 = np.meshgrid(x1, x2)    
        plot_X = np.c_[X1.ravel(), X2.ravel()]

        # 格子データを学習済モデルに入力し、予測値を算出
        plot_y = clf.predict(plot_X)

        # グラフ設定
        plt.figure(figsize=(fig_size_x, fig_size_y))
        ax = plt.axes()
        plt.rcParams['font.family'] = 'Times New Roman'  # 全体のフォント
        plt.rcParams['font.size'] = lim_font_size  # 全体のフォント
        plt.rcParams['axes.linewidth'] = 1.0    # 軸の太さ

        # 散布図のプロット
        for idx, (class_data, class_color) in enumerate(zip(class_datas, class_colors)):
            # 格子データをプロットし、決定境界を描画
            plt.scatter(plot_X.T[0][plot_y == class_data], plot_X.T[1][plot_y == class_data], marker='o', color=class_color, alpha=0.1)
            # 学習用データをプロット
            plt.scatter(train_X.T[0][train_y == class_data], train_X.T[1][train_y == class_data], marker='o', label=str(class_data), color=class_color, alpha=1.0)

        plt.legend(loc=1)           # 凡例の表示（2：位置は第二象限）
        plt.title("Decision boundary (" + x1_name + ", " + x2_name + ")", fontsize=lim_font_size)   # グラフタイトル
        plt.xlabel(x1_name, fontsize=lim_font_size)            # x軸ラベル
        plt.ylabel(x2_name, fontsize=lim_font_size)            # y軸ラベル

        plt.grid()                              # グリッドの表示
        # plt.show()
        plt.savefig(save_graph_img_path)
        plt.close() # バッファ解放

def main():
    # 学習済みモデルデータの出力先パス
    SAVE_TRAINED_DATA_PATH = '/Users/panzer5/github/sample/python/scikit/svm/ex5_data/train.learn'

    # グラフ出力先パス
    SAVE_GRAPH_IMG_PATH = '/Users/panzer5/github/sample/python/scikit/svm/ex5_data/graph_x2_x3.png'

    # SVMのパラメータ
    GAMMA = 0.1
    C = 1
    KERNEL = "rbf"

    # クラスのデータとプロット時に割り当てる色
    CLASS_DATAS = [0, 1, 2]
    CLASS_COLORS = ["blue", "red", "green"]

    svm = SVM()

    # 学習用のデータを読み込み(Irisデータセットを利用)
    iris_dataset = load_iris()

    # 説明変数（学習データ）を抽出
    X = iris_dataset.data

    # 目的変数：アヤメの品種（'setosa'=0 'versicolor'=1 'virginica'=2）
    y = iris_dataset.target 
    
    X1 = np.vstack((X[:, :1]))  #sepal lengthのみを取得
    X2 = np.vstack((X[:, 1:2])) #sepal widthのみを取得
    X3 = np.vstack((X[:, 2:3])) #petal lengthのみを取得
    X4 = np.vstack((X[:, 3:4])) #petal widthのみを取得
    
    # 学習に使用する説明変数を選択
    X = np.hstack((X1, X2, X3, X4))
    #X = np.hstack((X1, X2))
    #X = np.hstack((X2, X3))
    #X = np.hstack((X3, X4))

    # 説明変数のデータを、学習用データと検証用データに分割
    train_X, test_X, train_y, test_y = train_test_split(X, y, random_state = 0)

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
    predict_y = svm.predict(
        load_trained_data_path = SAVE_TRAINED_DATA_PATH,
        test_X=test_X)

    print("test_X:", test_X)
    print("predict_y:", predict_y)

    """
    # グラフにプロットして決定境界を可視化(説明変数２つで学習したときのみ利用可能)
    svm.plot2d(load_trained_data_path = SAVE_TRAINED_DATA_PATH,
        save_graph_img_path = SAVE_GRAPH_IMG_PATH,
        train_X=train_X,
        train_y=train_y,
        class_datas = CLASS_DATAS, 
        class_colors = CLASS_COLORS,
        x1_name = "x2",
        x2_name = "x3",
        fig_size_x = 10,
        fig_size_y = 10,
        lim_font_size = 25,   
    )
    """

    """
    Score： 0.9736842105263158

    test_X: [[5.8 2.8 5.1 2.4]
    [6.  2.2 4.  1. ]
    [5.5 4.2 1.4 0.2]
    [7.3 2.9 6.3 1.8]
    .....
    [5.2 2.7 3.9 1.4]
    [5.7 3.8 1.7 0.3]
    [6.  2.7 5.1 1.6]]

    predict_y: [2 1 0 2 0 2 0 1 1 1 2 1 1 1 1 0 1 1 0 0 2 1 0 0 2 0 0 1 1 0 2 1 0 2 2 1 0
    2]
    """

if __name__ == "__main__":
    main()
