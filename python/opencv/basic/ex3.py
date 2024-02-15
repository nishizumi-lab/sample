# -*- coding: utf-8 -*-
import cv2 as cv

# 入力画像のロード
img = cv.imread('/Users/github/sample/python/opencv/basic/mujiko.png')

# 画像をウィンドウに表示
cv.imshow("Mujiko Chan", img)

# キー入力待機
cv.waitKey(0)

# ウィンドウを廃棄
cv.destroyAllWindows()
