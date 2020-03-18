#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 入力画像を読み込み
img = cv2.imread(
    "C:/github/sample/python/opencv/threshold/dilate_erode/input.png")

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 二値化処理
gray[gray < 127] = 0
gray[gray >= 127] = 255

# カーネルの定義
kernel = np.ones((6, 6), np.uint8)

# 膨張・収縮処理(方法2)
dilate = cv2.dilate(gray, kernel)
erode = cv2.erode(dilate, kernel)

# 結果を出力
cv2.imwrite(
        "C:/github/sample/python/opencv/threshold/dilate_erode/dilate.png", dilate)
cv2.imwrite(
        "C:/github/sample/python/opencv/threshold/dilate_erode/erode.png", erode)

