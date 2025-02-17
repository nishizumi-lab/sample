#-*- coding:utf-8 -*-
import cv2 as cv

def DoM(gray, ksize1, ksize2):
    # カーネルサイズの異なる2つのメディアンフィルタ処理
    m1 = cv.medianBlur(gray, ksize1)
    m2 = cv.medianBlur(gray, ksize2)
    return m2 - m1

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/DoM/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# DoMフィルタの適用
dom_img = DoM(gray,3, 5)

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/DoM/output.png', dom_img)
