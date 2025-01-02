import cv2
import numpy as np

# 画像の読み込み(RGB)
img = cv2.imread("C:/github/sample/python/opencv/basic/input.png")

# img.shapeで画像の形状（高さ、幅、チャンネル数）を取得
# heightは画像の高さ、widthは幅、chはチャンネル数
height, width, ch = img.shape

# 画像の画素数を計算します
# 画素数は、画像の幅と高さの掛け算になります
size = width * height

# 画像の幅、高さ、チャンネル数、画素数、およびデータ型を表示します
# img.dtypeは、画像のデータ型を示します。
print("幅：", width)
print("高さ：", height)
print("チャンネル数:", ch)
print("画素数:", size)
print("データ型：", img.dtype)
print("shape属性", img.shape)


