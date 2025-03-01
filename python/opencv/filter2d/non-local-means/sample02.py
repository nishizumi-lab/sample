import cv2 as cv
import numpy as np

def update(val):
    # トラックバーの位置に基づいてパラメータを取得
    h = cv.getTrackbarPos('h', 'Non-Local Means Filter')
    hForColor = cv.getTrackbarPos('hForColor', 'Non-Local Means Filter')
    templateWindowSize = cv.getTrackbarPos('templateWindowSize', 'Non-Local Means Filter')
    searchWindowSize = cv.getTrackbarPos('searchWindowSize', 'Non-Local Means Filter')

    # 非局所的平均フィルタを適用
    filtered = cv.fastNlMeansDenoisingColored(img, None, h, hForColor, templateWindowSize, searchWindowSize)

    # フィルタ処理後の画像を表示
    cv.imshow('Non-Local Means Filter', filtered)

# 入力画像を読み込む
img = cv.imread('C:/github/sample/python/opencv/filter2d/non-local-means/input.jpg')

# ウィンドウを作成
cv.namedWindow('Non-Local Means Filter')

# トラックバーを作成
cv.createTrackbar('h', 'Non-Local Means Filter', 10, 50, update)
cv.createTrackbar('hForColor', 'Non-Local Means Filter', 10, 50, update)
cv.createTrackbar('templateWindowSize', 'Non-Local Means Filter', 7, 21, update)
cv.createTrackbar('searchWindowSize', 'Non-Local Means Filter', 21, 50, update)

# 初期表示
update(0)

# ユーザーが 'q' キーを押すまで待機
while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break