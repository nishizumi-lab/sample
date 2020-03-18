#-*- coding:utf-8 -*-
import cv2
    
# 入力画像の読み込み
img = cv2.imread("C:\prog\python\input.png")
    
# グレースケール変換   
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
# グレースケール画像の書き込み
cv2.imwrite("C:\prog\python\gray.png", gray)


# BGR, B, G, R, Grayの2次元配列を確認
print("BGR=", img)
print("-------------")

print("Blue=", img[:,:,0])
print("-------------")

print("Green=", img[:,:,1])
print("-------------")

print("Red=", img[:,:,2])
print("-------------")
print("gray=", gray)