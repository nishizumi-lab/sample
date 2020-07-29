#-*- coding:utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def plot_graph():

    # ファイルパス
    LOAD_CSV_PATH = "C:/github/sample/python/matplotlib/axis/axis2/csv/data.csv"
    SAVE_FIG_PATH = "C:/github/sample/python/matplotlib/axis/axis2/result/ex2.png"

    # CSVファイルのロード
    df = pd.read_csv(LOAD_CSV_PATH)
    df.index = df["time"]

    # figureオブジェクトを作成
    fig, ax1 = plt.subplots(figsize=(12.0, 7.0))

    # ax1とax2を関連させる
    ax2 = ax1.twinx()

    # フォントの種類
    plt.rcParams["font.family"] = "Times New Roman"

    # データの時間範囲
    min_time_soc100 = 4
    max_time_soc100 = min_time_soc100 + 11

    min_time_soc80 = 14
    max_time_soc80 = min_time_soc80 + 11

    min_time_soc60 = 24
    max_time_soc60 = min_time_soc60 + 11

    min_time_soc40 = 34
    max_time_soc40 = min_time_soc40 + 11

    # 電流、電圧、時間データを抽出
    I_soc100 = df.loc[min_time_soc100:max_time_soc100, "current"]
    V_soc100 = df.loc[min_time_soc100:max_time_soc100, "voltage"]
    time_soc100 = df.loc[min_time_soc100:max_time_soc100, "time"] - min_time_soc100

    I_soc80 = df.loc[min_time_soc80:max_time_soc80, "current"]
    V_soc80 = df.loc[min_time_soc80:max_time_soc80, "voltage"]
    time_soc80 = df.loc[min_time_soc80:max_time_soc80, "time"] - min_time_soc80

    I_soc60 = df.loc[min_time_soc60:max_time_soc60, "current"]
    V_soc60 = df.loc[min_time_soc60:max_time_soc60, "voltage"]
    time_soc60 = df.loc[min_time_soc60:max_time_soc60, "time"] - min_time_soc60

    I_soc40 = df.loc[min_time_soc40:max_time_soc40, "current"]
    V_soc40 = df.loc[min_time_soc40:max_time_soc40, "voltage"]
    time_soc40 = df.loc[min_time_soc40:max_time_soc40, "time"] - min_time_soc40

    # グラフ横軸の範囲
    graph_min_x = time_soc100.min()
    graph_max_x = time_soc100.max()

    # 第1軸に電圧データをプロット
    ax1.plot(time_soc100, V_soc100, "r--", label="$V SOC100$", linewidth=2)
    ax1.plot(time_soc80, V_soc80, "g--", label="$V SOC80$", linewidth=2)
    ax1.plot(time_soc60, V_soc60, "b--", label="$V SOC60$", linewidth=2)
    ax1.plot(time_soc40, V_soc40, "m--", label="$V SOC40$", linewidth=2)

    # 第2軸に電流データをプロット
    ax2.plot(time_soc100, I_soc100, "k--", label="$I_SOC100$", linewidth=2)

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
