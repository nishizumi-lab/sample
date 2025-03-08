# -*- coding:utf-8 -*-
import time
import cv2 as cv
import numpy as np


def DoG_filter(img, sigma=1, k =1.05, threshold = 30, ksize=5):

    # DoGフィルターのカーネルを計算
    # x と y のグリッドを作成
    x, y = np.meshgrid(np.arange(-ksize//2+1, ksize//2+1), np.arange(-ksize//2+1, ksize//2+1))
    kernel1 = np.exp(-(x**2 + y**2) / (2 * sigma**2))/(2 * np.pi * sigma**2)
    sigma2 = k*sigma
    kernel2 = np.exp(-(x**2 + y**2) / (2 * sigma2**2))/(2 * np.pi * sigma2**2)
    kernel = kernel2 - kernel1

    # 絶対値の総和で割って正規化
    kernel = kernel / np.sum(np.abs(kernel))

    # 畳み込み演算
    dog = cv.filter2D(img, -1, kernel)

    # 二値化処理
    _, binary = cv.threshold(dog, threshold, 255, cv.THRESH_BINARY)

    return binary

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/DoG/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 処理時間の計測開始
start_time = time.perf_counter()

# LoGフィルタ
log_img = DoG_filter(gray, sigma=1.0, k=1.09, threshold = 5, ksize=5)

# 処理時間の計測終了
end_time = time.perf_counter()

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/DoG/output2.png', log_img)

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))
# Processing Time: 0.002470 seconds