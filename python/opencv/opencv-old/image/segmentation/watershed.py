# -*- coding:utf-8 -*-
import numpy as np
import cv2

def main():
    im = cv2.imread("test.jpg")                         # 入力画像の取得
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)          # グレースケール変換
    th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1] # 2値化
    k = np.ones((3,3),np.uint8)                         # カーネルの定義
    bg = cv2.dilate(th,k,iterations=3)                  # 背景領域の抽出
    trans = cv2.distanceTransform(bg,cv2.DIST_L2,3)     # 背景領域の距離変換
    fg = cv2.threshold(trans,0.1*trans.max(),255,0)[1]  # 距離変換した画像データを2値化して前景領域を抽出
    fg = np.uint8(fg)                                   # 未知の領域を検索
    unknown = cv2.subtract(bg,fg)
    marker = cv2.connectedComponents(fg)[1]             # ラベリング処理
    marker = marker + 1
    marker[unknown == 255] = 0                          # 未知領域を0で塗り潰す
    marker = cv2.watershed(im,marker)                   # watershed法で領域分割
    im[marker == -1] = [0,255,0]                        # 領域の境界（-1）を緑色でり潰
    cv2.imshow("watershed",im)                          # 画像の表示
    cv2.waitKey(0)                                      # キー入力待機
    cv2.destroyAllWindows()                             # ウィンドウ廃棄


if __name__ == "__main__":
    main()
