# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 入力画像の読み込み
img = cv2.imread("C:/github/sample/python/opencv/resize/input.png")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

theta = 45  # 回転角
scale = 1.0    # 回転角度・拡大率

# 画像の中心座標
oy, ox = int(gray.shape[0]/2), int(gray.shape[1]/2)

# 方法2(OpenCV)
R = cv2.getRotationMatrix2D((ox, oy), theta, scale)    # 回転変換行列の算出
dst = cv2.warpAffine(gray, R, gray.shape,
                     flags=cv2.INTER_CUBIC)    # アフィン変換

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/resize/affine1.png", dst)
