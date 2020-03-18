# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 矢印を描画する
def drow_arrow(im, pt1, pt2, color, thickness=1, line_type=8, shift=0, w=5, h=10):
    vx = pt2[0] - pt1[0]
    vy = pt2[1] - pt1[1]
    v  = np.sqrt(vx ** 2 + vy ** 2)
    ux = vx / v
    uy = vy / v
    ptl = (int(pt2[0] - uy*w - ux*h), int(pt2[1] + ux*w - uy*h))
    ptr = (int(pt2[0] + uy*w - ux*h), int(pt2[1] - ux*w - uy*h))
    cv2.line(im, pt1, pt2, color, thickness, line_type, shift)
    cv2.line(im, pt2, ptl, color, thickness, line_type, shift)
    cv2.line(im, pt2, ptr, color, thickness, line_type, shift)

def main():
    # 入力画像の取得
    im = cv2.imread("test.jpg")
    # 画像に矢印を描く
    drow_arrow(im, (50,50), (150,150), (0,0,200), 5)
    # ウィンドウ表示
    cv2.imshow("Test", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
