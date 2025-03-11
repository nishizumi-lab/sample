#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 輪郭検出を更新する関数
def update_edges(val):
    # トラックバーの現在の最小閾値を取得
    min_thresh = cv.getTrackbarPos('Min Threshold', 'Edges')
    # トラックバーの現在の最大閾値を取得
    max_thresh = cv.getTrackbarPos('Max Threshold', 'Edges')
    # Cannyアルゴリズムの適用
    edges = cv.Canny(gray, min_thresh, max_thresh)
    # 輪郭画像の表示
    cv.imshow('Edges', edges)


# 入力画像を読み込み
img = cv.imread("C:/github/sample/python/opencv/filter2d/canny/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# ウィンドウの作成
cv.namedWindow('Edges')

# トラックバーの作成
cv.createTrackbar('Min Threshold', 'Edges', 50, 255, update_edges)
cv.createTrackbar('Max Threshold', 'Edges', 100, 255, update_edges)

# 初期エッジ画像の表示
update_edges(0)

# キー入力があればウィンドウを閉じる
cv.waitKey(0)
cv.destroyAllWindows()