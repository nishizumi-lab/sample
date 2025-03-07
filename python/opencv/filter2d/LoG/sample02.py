# -*- coding:utf-8 -*-
import time
import cv2 as cv
import numpy as np


def LoG_filter(img, sigma=3, threshold = 30, ksize=5):

    # LoGフィルターのカーネルを計算
    # x と y のグリッドを作成
    x, y = np.meshgrid(np.arange(-ksize//2+1, ksize//2+1), np.arange(-ksize//2+1, ksize//2+1))

    # LoGのカーネルを計算する式
    kernel = (x**2 + y**2 - 2*sigma**2)/(2 * np.pi * sigma**6) * np.exp(-(x**2 + y**2) / (2 * sigma**2))

    # 絶対値の総和で割って正規化(カーネルの絶対値の合計が1になる)
    kernel = kernel / np.sum(np.abs(kernel))

    # 畳み込み演算
    log = cv.filter2D(img, cv.CV_64F, kernel)

    # 二値化処理
    _, binary = cv.threshold(log, threshold, 255, cv.THRESH_BINARY)

    return binary

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/LoG/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 処理時間の計測開始
start_time = time.perf_counter()

# LoGフィルタ
log_img = LoG_filter(gray, sigma=1.0, threshold = 5, ksize=5)

# 処理時間の計測終了
end_time = time.perf_counter()

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/LoG/output2.png', log_img)

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))
# Processing Time: 0.007971 seconds