#-*- coding:utf-8 -*-
import cv2 as cv

def LoG(gray, ksize, sigma, threshold):
    # Gaussianフィルタで画像をぼかす
    blurred = cv.GaussianBlur(gray, (ksize, ksize), sigma)

    # Laplacianフィルタを適用
    log = cv.Laplacian(blurred, cv.CV_64F)

    # 二値化処理
    _, binary = cv.threshold(log, threshold, 255, cv.THRESH_BINARY)
    
    return binary

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/LoG/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# LoGフィルタの適用
log_img = LoG(gray, 3, 1.0, 30)

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/LoG/output.png', log_img)
