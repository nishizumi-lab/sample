#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 畳み込み処理
def filter2d(src, kernel, fill_value=-1):
    # カーネルサイズ
    m, n = kernel.shape
    
    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)

    # 入力画像の高さと幅
    h, w = src.shape[0], src.shape[1]
    
    # 出力画像用の配列
    if fill_value == -1: 
        dst = src.copy()
    elif fill_value == 0: 
        dst = np.zeros((h, w))
    else:
        dst = np.zeros((h, w))
        dst.fill(fill_value)

    # 畳み込み演算
    for y in range(d, h - d):
        for x in range(d, w - d):
            dst[y][x] = np.sum(src[y-d:y+d+1, x-d:x+d+1] * kernel)
            
    return dst
    

# 入力画像をグレースケールで読み込み
gray = cv2.imread("C:/github/sample/python/opencv/filter2d/blur/input.png", 0)
    
# カーネル
kernel = np.array([[1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9]])

# 方法1(NumPyで実装)
dst = filter2d(gray, kernel, -1)
    
# 結果を出力
cv2.imwrite("C:/github/sample/python/opencv/filter2d/blur/output.png", dst)
