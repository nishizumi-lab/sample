#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 膨張処理
def dilate(src, ksize=3):
    # 入力画像のサイズを取得
    h, w = src.shape
    # 入力画像をコピーして出力画像用配列を生成
    dst = src.copy()
    # 注目領域の幅
    d = int((ksize-1)/2)

    for y in range(0, h):
        for x in range(0, w):
            # 近傍に白い画素が1つでもあれば、注目画素を白色に塗り替える
            roi = src[y-d:y+d+1, x-d:x+d+1]
            if np.count_nonzero(roi) > 0:
                dst[y][x] = 255

    return dst

# 収縮処理
def erode(src, ksize=3):
    # 入力画像のサイズを取得
    h, w = src.shape
    # 入力画像をコピーして出力画像用配列を生成
    dst = src.copy()
    # 注目領域の幅
    d = int((ksize-1)/2)

    for y in range(0, h):
        for x in range(0, w):
            # 近傍に黒い画素が1つでもあれば、注目画素を黒色に塗り替える
            roi = src[y-d:y+d+1, x-d:x+d+1]
            if roi.size - np.count_nonzero(roi) > 0:
                dst[y][x] = 0

    return dst


# 入力画像を読み込み
img = cv.imread(
    "/Users/github/sample/python/opencv/threshold/dilate_erode/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 二値化処理
gray[gray<127] = 0
gray[gray>=127] = 255

# 膨張・収縮処理(方法1)
dilate_img = dilate(gray, ksize=6)
erode_img = erode(dilate_img, ksize=6)

# 結果を出力
cv.imwrite(
    "/Users/github/sample/python/opencv/threshold/dilate_erode/dilate.png", dilate_img)
cv.imwrite(
    "/Users/github/sample/python/opencv/threshold/dilate_erode/erode.png", erode_img)
