#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


# 入力画像を読み込み
img = cv.imread("/Users/github/sample/python/opencv/histgram/input.jpg")

img_b, img_g, img_r = img[:,:,0], img[:,:,1], img[:,:,2]

# 方法1(NumPyでヒストグラムの算出)
# hist_r, bins = np.histogram(r.ravel(),256,[0,256])
# hist_g, bins = np.histogram(g.ravel(),256,[0,256])
# hist_b, bins = np.histogram(b.ravel(),256,[0,256])

# 方法2(OpenCVでヒストグラムの算出)
hist_r = cv.calcHist([img_r],[0],None,[256],[0,256])
hist_g = cv.calcHist([img_g],[0],None,[256],[0,256])
hist_b = cv.calcHist([img_b],[0],None,[256],[0,256])

print('hist_r=')
print(hist_r)

print('hist_g=')
print(hist_g)

print('hist_b=')
print(hist_b)

# グラフの作成
plt.xlim(0, 255)
plt.plot(hist_r, "-r", label="Red")
plt.plot(hist_g, "-g", label="Green")
plt.plot(hist_b, "-b", label="Blue")
plt.xlabel("Pixel value", fontsize=20)
plt.ylabel("Number of pixels", fontsize=20)
plt.legend()
plt.grid()
plt.show()