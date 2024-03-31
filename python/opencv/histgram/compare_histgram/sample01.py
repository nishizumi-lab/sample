#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def calc_hist(img):
    # ヒストグラムを計算
    hist = cv.calcHist([img], channels=[0], mask=None, histSize=[256], ranges=[0, 256])
    # ヒストグラムを正規化
    hist = cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)
    # (n_bins, 1) -> (n_bins,)
    hist = hist.squeeze(axis=-1)

    return hist

def main():
    # 入力画像を読み込み
    # 入力画像を読み込み
    img1 = cv.imread("/Users/images/00000-1095803260.png", cv.IMREAD_GRAYSCALE)
    img2 = cv.imread("/Users/images/00000-1586254068.png", cv.IMREAD_GRAYSCALE)
    img3 = cv.imread("/Users/images/00000-4130983791.png", cv.IMREAD_GRAYSCALE)
    img4 = cv.imread("/Users/images/00001-750780685.png", cv.IMREAD_GRAYSCALE)
        
    hist1 = calc_hist(img1)
    hist2 = calc_hist(img2)
    hist3 = calc_hist(img3)
    hist4 = calc_hist(img4)  
    
    score12 = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)
    score23 = cv.compareHist(hist2, hist3, cv.HISTCMP_CORREL)
    score14 = cv.compareHist(hist1, hist4, cv.HISTCMP_CORREL)
        
    print(f"hist1とhist2の類似度は{score12}")
    print(f"hist2とhist3の類似度は{score23}")
    print(f"hist1とhist4の類似度は{score14}")
    
main()

