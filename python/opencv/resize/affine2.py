# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np

# アフィン変換で画像配列の回転
def rotate_affine(src, theta):
    # 元画像のサイズを取得
    h, w = src.shape[0], src.shape[1]

    # 出力画像用の配列生成（要素は全て0）
    dst = np.zeros((h, w))

    # degreeかｒradianに変換
    rd = np.radians(theta)


    # アフィン変換
    for y in range(0, h):
        for x in range(0, w):
            xi = (x - int(w/2))*np.cos(rd) - (y - int(h/2))*np.sin(rd) + int(w/2)
            yi = (x - int(w/2))*np.sin(rd) + (y - int(h/2))*np.cos(rd) + int(h/2)
            xi = int(xi)
            yi = int(yi)

            # 変換後の座標が範囲外でなければ出力画像配列に画素値を代入
            if yi < h - 1 and xi < w - 1 and yi > 0 and xi > 0:
                dst[y][x] = src[yi][xi]

    return dst

# 入力画像の読み込み
img = cv.imread("/Users/github/sample/python/opencv/resize/input.png")
    
# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

theta = 45  # 回転角

# 方法(NumPy）
dst = rotate_affine(gray, theta)

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/resize/affine2.png", dst)
