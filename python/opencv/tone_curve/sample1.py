#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/tone_curve/input.jpg")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 線形濃度変換
a, k = 0.7, 20
zmin, zmax = 20.0, 220.0

# 変換1
# gray = a * gray    

# 変換2
# gray = gray + k    

# 変換3
gray = a * (gray - 127.0) + 127.0

# 変換4
#gray = gray.max() * (gray - zmin)/(zmax - zmin) 

# 画素値を0～255の範囲内に収める
gray[gray < 0] = 0
gray[gray > 255] = 255

# 結果の出力
cv.imwrite("C:/github/sample/python/opencv/tone_curve/output1.jpg", gray)
