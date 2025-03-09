# -*- coding:utf-8 -*-
import time
import cv2 as cv
import numpy as np

def DoM(gray, ksize1=5, ksize2=3, ksize3=6, threshold=50):
    
    # カーネルサイズの異なる2つのメディアンフィルタ処理
    blur1 = cv.blur(gray, (ksize1, ksize1))
    blur2 = cv.blur(gray, (ksize2, ksize2))

    # 二値化処理
    _, binary = cv.threshold(blur2 - blur1, threshold, 255, cv.THRESH_BINARY)

    # カーネルの定義
    kernel = np.ones((ksize3, ksize3), np.uint8)

    # 収縮処理(細線化)
    erode = cv.erode(binary , kernel)

    return erode

# 入力画像を読み込み
img = cv.imread('C:/github/sample/python/opencv/filter2d/DoM/input.png')

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# 処理時間の計測開始
start_time = time.perf_counter()

# DoMフィルタの適用
dom_img = DoM(gray, ksize1=5, ksize2=3, ksize3=2,threshold=10)

# 処理時間の計測終了
end_time = time.perf_counter()

# 結果を保存
cv.imwrite('C:/github/sample/python/opencv/filter2d/DoM/output2.png', dom_img)

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))
# Processing Time: 0.006521 seconds
