#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
    
# 入力画像をグレースケールで読み込み
gray = cv.imread("/Users/github/sample/python/opencv/filter2d/emboss/input.png", 0)
    
# カーネル（オペレータ）
kernel = np.array([[-2, -1, 0],
                    [-1, 1, 1],
                    [-1, 1, 2]])

# オフセット値
offset = 128
    
    
# フィルタ処理     
dst2 = cv.filter2D(gray, -1, kernel, delta=offset)
    
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/emboss/output2.png", dst2)
