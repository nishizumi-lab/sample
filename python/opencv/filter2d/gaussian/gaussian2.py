#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像を読み込み
img = cv2.imread("C:/github/sample/python/opencv/filter2d/gaussian/input.png")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# カーネル
kernel = np.array([[1/16, 1/8, 1/16],
                   [1/8, 1/4, 1/8],
                   [1/16, 1/8, 1/16]])

# 方法2
dst = cv2.filter2D(gray, -1, kernel)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/filter2d/gaussian/output.png", dst)
