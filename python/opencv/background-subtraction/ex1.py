# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import time

i = 0      # カウント変数
th = 30    # 差分画像の閾値

# 動画ファイルのキャプチャ
cap = cv.VideoCapture(
    "/Users/github/sample/python/opencv/dataset/videos/red_marker.mp4")

# 最初のフレームを背景画像に設定
ret, bg = cap.read()

# グレースケール変換
bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)

while(cap.isOpened()):
    # フレームの取得
    ret, frame = cap.read()

    # グレースケール変換
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 差分の絶対値を計算
    mask = cv.absdiff(gray, bg)

    # 差分画像を二値化してマスク画像を算出
    mask[mask < th] = 0
    mask[mask >= th] = 255

    # フレームとマスク画像を表示
    cv.imshow("Mask", mask)
    cv.imshow("Flame", gray)
    cv.imshow("Background", bg)

    # 待機(0.03sec)
    time.sleep(0.03)
    i += 1    # カウントを1増やす

    # 背景画像の更新（一定間隔）
    if(i > 30):
        ret, bg = cap.read()
        bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
        i = 0  # カウント変数の初期化

    # qキーが押されたら途中終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
