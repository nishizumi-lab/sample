#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像を読み込み
img = cv2.imread("C:/github/sample/python/opencv/tone_curve/input.jpg")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 線形濃度変換
gamma = 0.5

# 画素値の最大値
imax = gray.max()

# ガンマ補正
gray = imax * (gray / imax)**(1/gamma)

# 結果の出力
cv2.imwrite("C:/github/sample/python/opencv/tone_curve/output2.jpg", gray)
