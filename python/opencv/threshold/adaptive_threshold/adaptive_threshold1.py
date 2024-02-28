#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

def threshold(src, ksize=3, c=2):
    
    # 局所領域の幅
    d = int((ksize-1)/2)

    # 画像の高さと幅
    h, w = src.shape[0], src.shape[1]
    
    # 出力画像用の配列（要素は全て255）
    dst = np.empty((h,w))
    dst.fill(255)
    
    # 局所領域の画素数
    N = ksize**2

    for y in range(0, h):
        for x in range(0, w):
            # 局所領域内の画素値の平均を計算し、閾値に設定
            t = np.sum(src[y-d:y+d+1, x-d:x+d+1]) / N

            # 求めた閾値で二値化処理
            if(src[y][x] < t - c): dst[y][x] = 0
            else: dst[y][x] = 255

    return dst
    

# 入力画像を読み込み
img = cv.imread(
    "/Users/github/sample/python/opencv/threshold/adaptive_threshold/input.jpg")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 方法1
dst = threshold(gray, ksize=11, c=13)

# 結果を出力
cv.imwrite(
    "/Users/github/sample/python/opencv/threshold/adaptive_threshold/output.jpg", dst)
