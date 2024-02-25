#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np

# 入力画像の取得
img = cv.imread("/Users/github/sample/python/opencv/labeling/input.png")

# グレースケール変換
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 2値化
gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

# ラベリング処理
label = cv.connectedComponentsWithStats(gray)

# ブロブ情報を項目別に抽出
n = label[0] - 1
data = np.delete(label[2], 0, 0)
center = np.delete(label[3], 0, 0)

# ラベルの個数nだけ色を用意
print("ブロブの個数:", n)
print("各ブロブの外接矩形の左上x座標", data[:,0])
print("各ブロブの外接矩形の左上y座標", data[:,1])
print("各ブロブの外接矩形の幅", data[:,2])
print("各ブロブの外接矩形の高さ", data[:,3])
print("各ブロブの面積", data[:,4])
print("各ブロブの中心座標:\n",center)

"""
■実行結果

ブロブの個数: 3
各ブロブの外接矩形の左上x座標 [ 18 188 201]
各ブロブの外接矩形の左上y座標 [ 17  39 133]
各ブロブの外接矩形の幅 [157  99  86]
各ブロブの外接矩形の高さ [195  69  72]
各ブロブの面積 [24025  6831  4959]
各ブロブの中心座標:
 [[ 96.03862643 114.05739854]
 [237.          73.        ]
 [239.72554951 174.98648921]]
"""

