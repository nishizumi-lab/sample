# -*- coding: utf-8 -*-
import cv2 as cv

# 出力先の動画ファイルパス
filepath = '/Users/github/sample/python/opencv/video/output.avi'

# カメラのキャプチャ
cap = cv.VideoCapture(0)
fps = 30

# 録画する動画のフレームサイズ（webカメラと同じにする）
size = (640, 480)

# 出力する動画ファイルの設定
fourcc = cv.VideoWriter_fourcc(*'XVID')
video = cv.VideoWriter(filepath, fourcc, fps, size)

while (cap.isOpened()):
    ret, frame = cap.read()

    # 画面表示
    cv.imshow('frame', frame)

    # 書き込み
    video.write(frame)

    # キー入力待機
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 終了処理
cap.release()
video.release()
cv.destroyAllWindows()