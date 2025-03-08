# -*- coding:utf-8 -*-
import time
import cv2 as cv
import numpy as np

def custom_median_filter(img, ksize):
    # 中央値フィルタのカーネルを手動で適用
    pad_size = ksize // 2
    padded_img = np.pad(img, pad_size, mode='constant', constant_values=0)
    filtered_img = np.zeros_like(img)
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            neighborhood = padded_img[i:i+ksize, j:j+ksize]
            median_value = np.median(neighborhood)
            filtered_img[i, j] = median_value
    
    return filtered_img

def DoM(gray, ksize1, ksize2, threshold=50):
    # カーネルサイズの異なる2つのメディアンフィルタ処理
    median1 = custom_median_filter(gray, ksize1)
    median2 = custom_median_filter(gray, ksize2)
    
    # 二値化処理
    _, binary = cv.threshold(median2 - median1, threshold, 255, cv.THRESH_BINARY)

    return binary

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/DoM/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 処理時間の計測開始
start_time = time.perf_counter()

# DoMフィルタの適用
dom_img = DoM(gray, 5, 3)

# 処理時間の計測終了
end_time = time.perf_counter()

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/DoM/output.png', dom_img)

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))
# Processing Time: 0.005940 seconds
