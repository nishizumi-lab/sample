# -*- coding: utf-8 -*-
import cv2

# 入力画像のロード
img = cv2.imread('input.png')

cv2.imshow("input", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
