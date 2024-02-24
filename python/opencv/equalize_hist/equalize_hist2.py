#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

def equalize_hist(src):
    # 画像の高さ・幅を取得
    h, w = src.shape[0], src.shape[1]
    
    # 全画素数
    s = w * h
    
    # 画素値の最大値
    imax = src.max()
    
    # ヒストグラムの算出
    hist, bins = np.histogram(src.ravel(),256,[0,256])

    # 出力画像用の配列（要素は全て0）
    dst = np.empty((h,w))

    for y in range(0, h):
        for x in range(0, w):
            # ヒストグラム平均化の計算式
            dst[y][x] = np.sum(hist[0: src[y][x]]) * (imax / s)

    return dst


# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/equalize_hist/input.jpg")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 方法1(NumPyで実装)
dst = equalize_hist(gray)
    
# 結果の出力
cv.imwrite("/Users/github/sample/python/opencv/equalize_hist/output2.jpg", dst)
