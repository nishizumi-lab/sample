# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 点p0に一番近い点を点群psから抽出
def serch_neighbourhood(p0, ps):
    L = np.array([])
    for i in xrange(ps.shape[0]):
        L = np.append(L,np.linalg.norm(ps[i]-p0))
    return ps[np.argmin(L)]

def main():
    # 入力画像の取得
    im = cv2.imread("test.jpg")
    # グレースケール変換
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # 2値化
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # ラベリング処理
    label = cv2.connectedComponentsWithStats(gray)
    # ラベルの個数nと各ラベルの重心座標cogを取得
    n = label[0] - 1
    cog = np.delete(label[3], 0, 0)
    p0 = np.array([200, 10])
    p1 = serch_neighbourhood(p0, cog)
    cv2.circle(im,(int(p0[0]),int(p0[1])), 10, (0,250,0), -1)
    cv2.circle(im,(int(p1[0]),int(p1[1])), 10, (0,0,255), -1)
    cv2.line(im,(int(p0[0]),int(p0[1])),(int(p1[0]),int(p1[1])),(255,0,0),5)
    # ウィンドウ表示
    cv2.imshow("CoG", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
