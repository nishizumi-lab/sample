# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 最近傍補間法でリサイズ
def resize_nearest(src, h, w):
    # 出力画像用の配列生成（要素は全て空）
    dst = np.empty((h,w))

    # 元画像のサイズを取得
    hi, wi = src.shape[0], src.shape[1]

    # 拡大率を計算
    ax = w / float(wi)
    ay = h / float(hi)

    # 最近傍補間
    for y in range(0, h):
        for x in range(0, w):
            xi, yi = int(round(x/ax)), int(round(y/ay))
            # 存在しない座標の処理
            if xi > wi -1: xi = wi -1
            if yi > hi -1: yi = hi -1

            dst[y][x] = src[yi][xi]

    return dst


# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/resize/input.png")
    
# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 方法1(NumPy）
dst = resize_nearest(gray, gray.shape[1]*2, gray.shape[0]*2)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/resize/nearest1.png", dst)
