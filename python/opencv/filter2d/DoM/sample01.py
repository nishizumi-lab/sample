#-*- coding:utf-8 -*-
import time
import cv2 as cv

def DoM(gray, ksize1, ksize2, threshold=50):
    # カーネルサイズの異なる2つのメディアンフィルタ処理
    median1 = cv.medianBlur(gray, ksize1)
    median2 = cv.medianBlur(gray, ksize2)
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
cv.imwrite('C:/github/sample/python/opencv/filter2d/DoM/output1.png', dom_img)

# 処理時間の表示
print("Processing Time: {:.6f} seconds".format(end_time - start_time))
# Processing Time: 0.005940 seconds