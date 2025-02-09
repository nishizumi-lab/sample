#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np


def emboss_filter(src, kernel, offset=128):
    # カーネルサイズ
    m, n = kernel.shape

    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)
    h, w = src.shape[0], src.shape[1]

    # 出力画像用の配列（要素は全てoffset値）
    dst = np.empty((h, w))
    dst.fill(offset)

    for y in range(d, h - d):
        for x in range(d, w - d):
            # 畳み込み演算
            dst[y][x] = np.sum(src[y-d:y+d+1, x-d:x+d+1]*kernel) + offset


    return dst


# 入力画像をグレースケールで読み込み
gray = cv.imread(
        "/Users/github/sample/python/opencv/filter2d/emboss/input.png", 0)

# カーネル（オペレータ）
kernel = np.array([[-2, -1, 0],
                    [-1, 1, 1],
                    [-1, 1, 2]])

# オフセット値
offset = 128

# フィルタ処理
dst1 = emboss_filter(gray, kernel, offset)

# 結果を出力
cv.imwrite(
        "/Users/github/sample/python/opencv/filter2d/emboss/output.png", dst1)
