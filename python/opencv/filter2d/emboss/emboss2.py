#-*- coding:utf-8 -*-
import cv2
import numpy as np
    
# 入力画像をグレースケールで読み込み
gray = cv2.imread("input.jpg", 0)
    
# カーネル（オペレータ）
kernel = np.array([[-2, -1, 0],
                    [-1, 1, 1],
                    [-1, 1, 2]])

# オフセット値
offset = 128
    
    
# 方法2       
dst2 = cv2.filter2D(gray, -1, kernel, delta=offset)
    
# 結果を出力
cv2.imwrite("output2.jpg", dst2)
