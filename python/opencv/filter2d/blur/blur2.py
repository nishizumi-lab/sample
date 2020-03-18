#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像をグレースケールで読み込み
gray = cv2.imread("C:/github/sample/python/opencv/filter2d/blur/input.png", 0)

# カーネル（縦方向の輪郭検出用）
kernel = np.array([[1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9]])

# 方法2(OpenCVで実装)
dst = cv2.filter2D(gray, -1, kernel)

# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/filter2d/blur/output.png", dst)
