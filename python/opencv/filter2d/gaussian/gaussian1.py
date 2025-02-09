#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

def gaussian_filter(src, kernel):
    # get kernel size
    # カーネルサイズ
    m, n = kernel.shape
    
    # width of skip
    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)
    h, w = src.shape[0], src.shape[1]
    
    # ndarray of destination
    # 出力画像用の配列（要素値は入力画像と同じ）
    dst = src.copy()

    # Spatial filtering
    for y in range(d, h - d):
        for x in range(d, w - d):
            dst[y][x] = np.sum(src[y-d:y+d+1, x-d:x+d+1]*kernel)
            
    return dst


# load image (grayscale)
# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/filter2d/gaussian/input.png")

# convert grayscale
# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    
# kernel of gaussian
# カーネル
kernel = np.array([[1/16, 1/8, 1/16],
                   [1/8, 1/4, 1/8],
                   [1/16, 1/8, 1/16]])

# Spatial filtering
# フィルタ処理
dst = gaussian_filter(gray, kernel)
    
# output
# 結果を出力
cv.imwrite("/Users/github/sample/python/opencv/filter2d/gaussian/output.png", dst)
