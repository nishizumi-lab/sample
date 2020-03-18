# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 重複要素の削除とソート
def unique2d(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

def main():
    im = cv2.imread("map.png")  # 入力画像を取得
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # マスク画像を用いて元画像から指定した色を抽出
    hsv_min = np.array([160,150,0])
    hsv_max = np.array([190,255,255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    x2,x1 = np.array(np.nonzero(mask))
    w = np.dstack((x1,x2))[0]/10
    cv2.imshow("View",mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()                     # ウィンドウ破棄
    w = unique2d(w)
    wz = np.zeros(w.shape[0])
    ws = np.c_[w.T[0],w.T[1],wz.T]
    np.savetxt("obst.csv",ws , delimiter="\t",fmt="%d")

if __name__ == '__main__':
    main()
