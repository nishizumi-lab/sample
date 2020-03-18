# -*- coding: utf-8 -*-
import cv2

def main():
    # 画像をグレースケールで取得
    im1 = cv2.imread("test1.jpg",0)
    im2 = cv2.imread("test2.jpg",0)
    # 画像のヒストグラム計算
    hist1 = cv2.calcHist([im1],[0],None,[256],[0,256])
    hist2 = cv2.calcHist([im2],[0],None,[256],[0,256])
    # ヒストグラムの類似度を計算
    d = cv2.compareHist(hist1,hist2,0)
    print(d)

if __name__ == "__main__":
    main()
