#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/diff/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# カーネル
kernel = np.array([[0, 0, 0],
                   [-1, 0, 1],
                   [0, 0, 0]])

# データ型がcv2.CV_8U(-1)
dst1 = cv.filter2D(gray, -1, kernel)

# データ型がcv2.CV_64F
dst2 = cv.filter2D(gray, cv.CV_64F, kernel)

# 画像配列の中身出力
print("dst1=\n", dst1)
print("\n\n")
print("dst2=\n", dst2)

# 結果を出力
cv.imwrite("C:/github/sample/python/opencv/filter2d/diff/output1.jpg", dst1)
cv.imwrite("C:/github/sample/python/opencv/filter2d/diff/output2.jpg", np.uint8(np.abs(dst2)))


