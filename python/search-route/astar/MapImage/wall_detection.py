# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 重複要素の削除とソート
def unique2d(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

def main():
    gray = cv2.imread("map.png",0)  # 入力画像をグレースケールで取得
    gray = 255 - gray
    x2,x1 = np.array(np.nonzero(gray))
    w = np.dstack((x1,x2))[0]/10
    cv2.destroyAllWindows()                     # ウィンドウ破棄
    w = unique2d(w)
    wz = np.zeros(w.shape[0])
    ws = np.c_[w.T[0],w.T[1],wz.T]
    np.savetxt("wall.csv",ws , delimiter="\t",fmt="%d")

if __name__ == '__main__':
    main()
