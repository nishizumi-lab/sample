#-*- coding:utf-8 -*-
import cv2
import numpy as np

# 動画ファイルのパス
filepath = "/Users/github/sample/python/opencv/video/input.mp4"

# 動画のキャプチャ
cap = cv2.VideoCapture(filepath)

# 動画のプロパティを取得
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
play_time = frame_num / fps

# 動画のプロパティを表示
print("WIDTH:", width)
print("HEIGHT:", height)
print("FPS:", fps)
print("FRAME NUM:", frame_num)
print("Play TIME[sec]:", play_time)

"""
WIDTH: 1280.0
HEIGHT: 720.0
FPS: 25.0
FRAME NUM: 2383.0
Play TIME[sec]: 95.32
"""
