# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
from datetime import timedelta

def main():
    # CSVファイルを読み込んでデータフレームに格納
    df = pd.read_csv("/Users/github/sample/python/pandas/csv/data4.csv")

    # ラベル毎の値を取り出し
    df['更新日時'] = pd.to_datetime(df['更新日時'], format='%Y-%m-%d %H:%M')

    # インデックスに「Time」列を設定
    df.set_index('更新日時', inplace=True)

    fig = plt.figure(1, figsize=(10,4))
    ax = fig.add_subplot(111)
    ax.plot(df.index, df["気温"], label="All")
    ax.legend(loc=1,fontsize=20)           # 凡例の表示（1：位置は第1象限）
    ax.grid()     
    ax.set_xlim(
        date2num([df.index.max() - timedelta(minutes=30),
                  df.index.max()]))
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    fig.savefig("/Users/github/sample/python/pandas/graph/sample01.png")

if __name__ == "__main__":
    main()