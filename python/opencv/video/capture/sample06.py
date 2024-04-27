#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# ファイルパス
filepath = "/Users/github/sample/python/opencv/video/input.mp4"

# 動画の読み込み
cap = cv.VideoCapture(filepath)

# 200フレーム目から取得
cap.set(cv.CAP_PROP_POS_FRAMES, 200)

# 動画終了まで繰り返し
while(cap.isOpened()):
    # フレームを取得
    ret, frame = cap.read()

    # フレームを表示
    cv.imshow("Frame", frame)

    # qキーが押されたら途中終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()