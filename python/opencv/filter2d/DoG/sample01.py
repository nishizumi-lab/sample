#-*- coding:utf-8 -*-
import cv2 as cv

# DoGフィルタ
def DoG(gray, ksize, sigma1, sigma2):
    # 標準偏差が異なる2つのガウシアン画像を算出
    g1 = cv.GaussianBlur(gray, ksize, sigma1)
    g2 = cv.GaussianBlur(gray, ksize, sigma2)
    # 2つのガウシアン画像の差分を出力
    return g1 - g2

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/DoG/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# LoGフィルタの適用
log_img = DoG(gray, (3,3), 3.2, 2.0)

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/DoG/output.png', log_img)
