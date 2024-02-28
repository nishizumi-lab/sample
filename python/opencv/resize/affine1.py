# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像の読み込み
img = cv.imread("/Users/github/sample/python/opencv/resize/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

theta = 45  # 回転角
scale = 1.0    # 回転角度・拡大率

# 画像の中心座標
oy, ox = int(gray.shape[0]/2), int(gray.shape[1]/2)

# 方法2(OpenCV)
R = cv.getRotationMatrix2D((ox, oy), theta, scale)    # 回転変換行列の算出
dst = cv.warpAffine(gray, R, gray.shape,
                     flags=cv.INTER_CUBIC)    # アフィン変換

# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/resize/affine1.png", dst)
