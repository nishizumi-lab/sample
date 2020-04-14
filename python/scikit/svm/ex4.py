# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import svm
import joblib
import matplotlib.pyplot as plt
from sklearn import metrics 

class SVM():
    # 学習
    def train(self,
        load_input_data_path,
        save_trained_data_path,
        name_x,
        name_y,
        gamma,
        C,
        kernel):

        # 学習用のデータを読み込み
        train_data = pd.read_csv(load_input_data_path, sep=",")

        # 説明変数：x1, x2
        train_X = train_data.loc[:, name_x].values

        # 目的変数：x3
        train_y = train_data[name_y].values

        # 学習（SVM）
        clf = svm.SVC(gamma=gamma, C=C, kernel=kernel)
        clf.fit(train_X, train_y)
        joblib.dump(clf, save_trained_data_path)

    # 検証
    def test(self,
        load_trained_data_path,
        load_test_data_path,
        name_x,
        name_y):

        # 学習済ファイルのロード
        clf = joblib.load(load_trained_data_path)

        # テスト用データの読み込み
        test_data = pd.read_csv(load_test_data_path, sep=",")

        # 説明変数：x1, x2
        test_X = test_data.loc[:, name_x].values

        # 正解データ：x3
        test_y = test_data[name_y].values

        # 学習結果の検証（テスト用データx1, x2を入力）
        predicted_y = clf.predict(test_X)

        # 正解データと予測データを比較し、スコアを計算
        score = metrics.accuracy_score(test_y, predicted_y)

        # 検証結果の表示
        print("Score：", score)

    # 予測
    def predict(self,
        load_trained_data_path,
        load_input_data_path,
        name_x,
        name_y):
        # 学習済ファイルのロード
        clf = joblib.load(load_trained_data_path)

        # 入力用データの読み込み
        test_data = pd.read_csv(load_input_data_path, sep=",")

        # 説明変数：x1, x2
        test_X = test_data.loc[:, name_x].values

        # 正解データ：x3
        test_y = test_data[name_y].values

        # モデルに入力し、予測値を計算
        predicted_y = clf.predict(test_X)
        
        return predicted_y

    # 決定境界のプロット
    def plot2d(self,
        load_input_data_path,
        load_trained_data_path,
        save_graph_img_path,
        class_datas, 
        class_colors,
        name_x,
        name_y,
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

        # 学習用のデータのロード
        train_data = pd.read_csv(load_input_data_path, sep=",")

        # 学習済ファイルのロード
        clf = joblib.load(load_trained_data_path)

        # 説明変数：x1, x2
        train_X = train_data.loc[:, name_x].values

        # 目的変数：x3
        train_y = train_data[name_y].values

        # 学習用データの説明変数の最大値、最小値を計算
        x1_min = train_X.T[0].min()
        x1_max = train_X.T[0].max()
        x2_min = train_X.T[1].min()
        x2_max = train_X.T[1].max()

        # 説明変数の最大値、最小値から格子データの範囲を計算
        if x1_0 == None:
            x1_0 = x1_min - 0.01 * (x1_max - x1_min)
        if x1_n == None:
            x1_n = x1_max + 0.01 * (x1_max - x1_min)

        if x2_0 == None:
            x2_0 = x2_min - 0.01 * (x2_max - x2_min)

        if x2_n == None:
            x2_n = x2_max + 0.01 * (x2_max - x2_min)

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
        plt.title('SVM TEST', fontsize=lim_font_size)   # グラフタイトル
        plt.xlabel(x1_name, fontsize=lim_font_size)            # x軸ラベル
        plt.ylabel(x2_name, fontsize=lim_font_size)            # y軸ラベル

        plt.grid()                              # グリッドの表示
        # plt.show()
        plt.savefig(save_graph_img_path)
        plt.close() # バッファ解放

def main():
    # 入力データのファイルパス
    LOAD_INPUT_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/svm/ex4_data/train.csv"

    # 学習済みモデルデータの出力先パス
    SAVE_TRAINED_DATA_PATH = '/Users/panzer5/github/sample/python/scikit/svm/ex4_data/train.learn'

    # テストデータのファイルパス
    LOAD_TEST_DATA_PATH = "/Users/panzer5/github/sample/python/scikit/svm/ex4_data/test.csv"

    # グラフ出力先パス
    SAVE_GRAPH_IMG_PATH = '/Users/panzer5/github/sample/python/scikit/svm/ex4_data/graph.png'

    # 説明変数の列名
    NAME_X = ["x1", "x2"]

    # 目的変数の列名
    NAME_Y = "x3"

    # SVMのパラメータ
    GAMMA = 0.1
    C = 1
    KERNEL = "rbf"

    # クラスのデータとプロット時に割り当てる色
    CLASS_DATAS = [0, 1, 2]
    CLASS_COLORS = ["blue", "red", "green"]

    svm = SVM()

    # 学習済みモデルの作成
    svm.train(load_input_data_path = LOAD_INPUT_DATA_PATH,
            save_trained_data_path = SAVE_TRAINED_DATA_PATH,
            name_x = NAME_X,
            name_y = NAME_Y,
            gamma = GAMMA,
            C = C,
            kernel = KERNEL)

    # 学習済みモデルの検証
    svm.test(
        load_trained_data_path = SAVE_TRAINED_DATA_PATH,
        load_test_data_path = LOAD_TEST_DATA_PATH,
        name_x = NAME_X,
        name_y = NAME_Y)

    # 未知データを入力して予測
    """
    svm.test(
        load_trained_data_path = SAVE_TRAINED_DATA_PATH,
        load_input_data_path = LOAD_INPUT_DATA_PATH,
        name_x = NAME_X,
        name_y = NAME_Y)
    """

    # グラフにプロットして決定境界を可視化
    svm.plot2d(
        load_input_data_path = LOAD_INPUT_DATA_PATH,
        load_trained_data_path = SAVE_TRAINED_DATA_PATH,
        save_graph_img_path = SAVE_GRAPH_IMG_PATH,
        class_datas = CLASS_DATAS, 
        class_colors = CLASS_COLORS,
        name_x = NAME_X,
        name_y = NAME_Y,
        x1_name = "x1",
        x2_name = "x2",
        fig_size_x = 10,
        fig_size_y = 10,
        lim_font_size = 22,   
    )


if __name__ == "__main__":
    main()
