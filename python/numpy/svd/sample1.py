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
    #train_data = df_csv.iloc[1:3000, 1]

    # 検証データ
    test_data = df_csv.iloc[0:6000, 1]

    w = 50  # width
    m = 2
    k = int(w/2)
    L = int(k/2)  # lag
    Tt = test_data.size
    score = np.zeros(Tt)

    for t in range(w+k, Tt-L+1+1):
        tstart = t-w-k+1
        tend = t-1
        X1 = embed(test_data[tstart:tend], w).T[::-1, :]  # trajectory matrix
        X2 = embed(test_data[(tstart+L):(tend+L)], w).T[::-1, :]  # test matrix

        U1, s1, V1 = np.linalg.svd(X1, full_matrices=True)
        U1 = U1[:, 0:m]
        U2, s2, V2 = np.linalg.svd(X2, full_matrices=True)
        U2 = U2[:, 0:m]

        U, s, V = np.linalg.svd(U1.T.dot(U2), full_matrices=True)
        sig1 = s[0]
        score[t] = 1 - np.square(sig1)

    # 異常度を正規化
    score = score / np.max(score)

    # グラフ作成
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    p1, = ax1.plot(score, '-b')
    ax1.set_ylabel('Abnormality')
    ax1.set_ylim(0, 1.2)
    p2, = ax2.plot(test_data, '-g')
    ax2.set_ylabel('Amplitude')
    ax2.set_ylim(0, 12.0)
    ax1.legend([p1, p2], ["Abnormality", "Test data"])
    ax1.grid()
    plt.savefig('C:/github/sample/python/numpy/svd/sample1.png')


def embed(lst, dim):
    emb = np.empty((0, dim), float)
    for i in range(lst.size - dim + 1):
        tmp = np.array(lst[i:i+dim]).reshape((1, -1))
        emb = np.append(emb, tmp, axis=0)
    return emb


if __name__ == '__main__':
    main()
