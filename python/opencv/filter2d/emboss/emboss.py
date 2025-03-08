#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
    
# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/emboss/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    
# カーネル（オペレータ）
kernel = np.array([[-2, -1, 0],
                    [-1, 1, 1],
                    [-1, 1, 2]])

# フィルタ処理     
dst2 = cv.filter2D(gray, -1, kernel, delta=128)
    
# 結果を出力
cv.imwrite("C:github/sample/python/opencv/filter2d/emboss/output.png", dst2)