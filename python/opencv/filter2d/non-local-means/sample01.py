#-*- coding:utf-8 -*-
import cv2 as cv


# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/bilateral/input.jpg')

# 非局所的平均フィルタを適用
filtered = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/bilateral/output.jpg', filtered)
