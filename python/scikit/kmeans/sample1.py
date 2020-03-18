# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import pandas as pd

def main():
    # CSVファイルの読み込み
    df_csv = pd.read_csv(
        "C:\github\sample\python\scikit\k-nearest-neighbor\ecg_dataset.csv")

    # 訓練データ
    train_data = df_csv.iloc[1:3000, 1]

    # 検証データ
    test_data = df_csv.iloc[3001:6000, 1]

    # 窓幅
    width = 100

    # K近傍法のk
    nk = 1

    # 窓幅を使ってベクトルの集合を作成
    train = embed(train_data, width)
    test = embed(test_data, width)

    # k近傍法でクラスタリング
    neigh = NearestNeighbors(n_neighbors=nk)
    neigh.fit(train)

    # 距離を計算
    d = neigh.kneighbors(test)[0] 

    # 距離の正規化
    mx = np.max(d)
    d = d / mx

 
    # グラフ作成
    fig = plt.figure(figsize=(10.0, 8.0))
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 12

    # 訓練データ
    plt.subplot(221)
    plt.plot(train_data, label='Training')
    plt.xlabel("Amplitude", fontsize=12)
    plt.ylabel("Sample", fontsize=12)
    plt.grid()
    leg = plt.legend(loc=1, fontsize=15)
    leg.get_frame().set_alpha(1)

    # 異常度
    plt.subplot(222)
    plt.plot(d, label='d')
    plt.xlabel("Amplitude", fontsize=12)
    plt.ylabel("Sample", fontsize=12)
    plt.grid()
    leg = plt.legend(loc=1, fontsize=15)
    leg.get_frame().set_alpha(1)

    # 検証用データ
    plt.subplot(223)
    plt.plot(test_data, label='Test')
    plt.xlabel("Amplitude", fontsize=12)
    plt.ylabel("Sample", fontsize=12)
    plt.grid()
    leg = plt.legend(loc=1, fontsize=15)
    leg.get_frame().set_alpha(1)

    plt.subplot(224)

    plt.savefig('C:/github/sample/python/scikit/k-nearest-neighbor/sample1.png')




def embed(lst, dim):
    emb = np.empty((0, dim), float)
    for i in range(lst.size - dim + 1):
        tmp = np.array(lst[i:i+dim])[::-1].reshape((1, -1))
        emb = np.append(emb, tmp, axis=0)
    return emb


if __name__ == '__main__':
    main()
