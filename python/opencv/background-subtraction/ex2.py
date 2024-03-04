# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import time

# フレーム差分の計算
def frame_sub(img1, img2, img3, th):
    # フレームの絶対差分
    diff1 = cv.absdiff(img1, img2)
    diff2 = cv.absdiff(img2, img3)

    # 2つの差分画像の論理積
    diff = cv.bitwise_and(diff1, diff2)

    # 二値化処理
    diff[diff < th] = 0
    diff[diff >= th] = 255
    
    # メディアンフィルタ処理（ゴマ塩ノイズ除去）
    mask = cv.medianBlur(diff, 3)

    return  mask


# 動画ファイルのキャプチャ
cap = cv.VideoCapture(
    "/Users/github/sample/python/opencv/dataset/videos/red_marker.mp4")
    
# フレームを3枚取得してグレースケール変換
frame1 = cv.cvtColor(cap.read()[1], cv.COLOR_RGB2GRAY)
frame2 = cv.cvtColor(cap.read()[1], cv.COLOR_RGB2GRAY)
frame3 = cv.cvtColor(cap.read()[1], cv.COLOR_RGB2GRAY)

while(cap.isOpened()):
    # フレーム間差分を計算
    mask = frame_sub(frame1, frame2, frame3, th=30)

    # 結果を表示
    cv.imshow("Frame2", frame2)
    cv.imshow("Mask", mask)

    # 3枚のフレームを更新
    frame1 = frame2
    frame2 = frame3
    frame3 = cv.cvtColor(cap.read()[1], cv.COLOR_RGB2GRAY)

    # 待機(0.03sec)
    time.sleep(0.03)

    # qキーが押されたら途中終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
