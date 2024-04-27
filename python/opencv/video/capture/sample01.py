#-*- coding:utf-8 -*-
import cv2 as cv

# 動画ファイルのパス
filepath = "/Users/github/sample/python/opencv/video/input.mp4"

# 動画のキャプチャ
cap = cv.VideoCapture(filepath)

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