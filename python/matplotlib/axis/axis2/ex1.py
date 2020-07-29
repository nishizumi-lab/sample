#-*- coding:utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def plot_graph():

    # ファイルパス
    LOAD_CSV_PATH = "C:/github/sample/python/matplotlib/axis/axis2/csv/data.csv"
    SAVE_FIG_PATH = "C:/github/sample/python/matplotlib/axis/axis2/result/ex1.png"

    # CSVファイルのロード
    df = pd.read_csv(LOAD_CSV_PATH)

    # figureオブジェクトを作成
    fig, ax1 = plt.subplots(figsize=(16.0, 8.0))

    # ax1とax2を関連させる
    ax2 = ax1.twinx()

    # フォントの種類
    plt.rcParams["font.family"] = "Times New Roman"

    # グラフ横軸の範囲
    graph_min_x = df["time"].min()
    graph_max_x = df["time"].max()

    # 第1軸に電圧データをプロット
    ax1.plot(df["time"], df["voltage"], "r--", label="$V$", linewidth=2)

    # 第2軸に電流データをプロット
    ax2.plot(df["time"], df["current"], "g-", label="$I$", linewidth=2)

    # 凡例を表示
    handler1, label1 = ax1.get_legend_handles_labels()
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler1 + handler2, label1 + label2, loc=1, borderaxespad=0.)
 
    # x軸の範囲を設定
    ax1.set_xlim([graph_min_x, graph_max_x])

    # 軸ラベルの設定
    ax1.set_xlabel("Time[s]")
    ax1.set_ylabel("Voltage[V]")
    ax2.set_ylabel("Current[A]")

    # 第1軸のグリッドを描画
    ax1.grid()

    # グラフをファイルに保存
    fig.savefig(SAVE_FIG_PATH)

    
def main():
    plot_graph()

if __name__ == "__main__":
    main()
