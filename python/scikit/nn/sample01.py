# -*- coding: utf-8
import numpy as np

# 活性化関数（ステップ関数）
def f(x):
    x = np.array(x)
    x[x>=0] = 1
    x[x<0] = -1
    return x

# 出力
def feed_forward(w, x):
    return f(np.dot(w, x))

# 学習
def train(w, x, t, eps):
    y = feed_forward(x, w)
    # 出力と正解が異なれば重み更新
    if(t != y):
        w += eps * t * x
    return w


def main():
    # パラメータ
    eps = 0.1 # 学習率
    max_epoch = 100 # エポック最大数（計算回数の最大値）

    # 教師データ
    X = np.array([[1,0,0], [1,0,1], [1,1,0], [1,1,1]], dtype=np.float32) # 入力
    t = np.array([-1,-1,-1,1], dtype=np.float32) # 正解ラベル

    # 重みの初期化(適当な値をセット)
    w  = np.array([0,0,0], dtype=np.float32)

    # 単純パーセプトロンで学習
    for e in range(max_epoch):
        # 学習
        for i in range(t.size):
            w = train(w, X[i], t[i], eps)

    # 検証
    y = f(np.sum(w*X, 1))
    print("出力：", y)
    print("正解：", t)
    print("重み：", w)

if __name__ == "__main__":
    main()