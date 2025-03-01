#-*- coding:utf-8 -*-
import cv2 as cv


# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/bilateral/input.jpg')

# バイラテラルフィルタを適用
dst = cv.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/bilateral/output.jpg', dst)
