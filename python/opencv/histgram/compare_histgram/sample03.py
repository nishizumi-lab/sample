#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
from pathlib import Path
import shutil

def calc_hist(img):
    # ヒストグラムを計算
    hist = cv.calcHist([img], channels=[0], mask=None, histSize=[256], ranges=[0, 256])
    # ヒストグラムを正規化
    hist = cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)
    # (n_bins, 1) -> (n_bins,)
    hist = hist.squeeze(axis=-1)

    return hist

def main():
    target_path = "/Users/images/"
    move_path = "/Users/images2/"
    target_img_path = "/Users/images/00000-217833465.png"

    img_paths = sorted(str(x) for x in Path(target_path).glob("*.png"))
    #print(img_paths)

    target_img = cv.imread(target_img_path, cv.IMREAD_GRAYSCALE)
    target_hist = calc_hist(target_img)

    for img_path in img_paths:
        # 画像を読み込む
        #print(str(img_path))
        img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
        # ヒストグラムを取得する
        hist = calc_hist(img)

        score = cv.compareHist(hist, target_hist, cv.HISTCMP_CORREL)
        
        if(score > 0.7):
            shutil.move(img_path, move_path)
            

        
main()

