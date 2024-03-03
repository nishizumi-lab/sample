#-*- coding:utf-8 -*-
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# 画像の読み込み
img = cv.imread("/Users/github/sample/python/opencv/equalize_hist/input2.jpg")

# RGB => YUV(YCbCr)
img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV) 
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB) 
 
# ヒストグラムの作成（引数の'image'を[ ]で囲うことを忘れないで下さい）
hist_img = cv.calcHist([img_yuv[:,:,0]], [0], None, [256], [0, 256])


# CLAHEオブジェクトを作成
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
dst_yuv = np.copy(img_yuv)
# CLAHEを適用
dst_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])

dst = cv.cvtColor(dst_yuv, cv.COLOR_YUV2BGR) # YUV => RGB
dst_rgb = cv.cvtColor(dst, cv.COLOR_BGR2RGB) 

# CLAHE適応後画像のヒストグラムの作成
hist_dst = cv.calcHist([dst_yuv[:,:,0]], [0], None, [256], [0, 256])

#dst = cv.medianBlur(dst, 5)

# 結果の出力
cv.imwrite('/Users/github/sample/python/opencv/equalize_hist/output3.jpg',dst)

# ヒストグラムの可視化
plt.rcParams["figure.figsize"] = [12,7.5]                         # 表示領域のアスペクト比を設定
plt.subplots_adjust(left=0.01, right=0.95, bottom=0.10, top=0.95) # 余白を設定
plt.subplot(221)                                                  # 1行2列の1番目の領域にプロットを設定
plt.imshow(img_rgb)                                    # 画像をRGBで表示
plt.axis("off")                                                   # 軸目盛、軸ラベルを消す
plt.subplot(222)                                                  # 1行2列の2番目の領域にプロットを設定
plt.plot(hist_img)                                               # ヒストグラムのグラフを表示
plt.xlabel('Brightness')                                          # x軸ラベル(明度)
plt.ylabel('Count')                                               # y軸ラベル(画素の数)

plt.subplot(223)                                                  # 1行2列の1番目の領域にプロットを設定
plt.imshow(dst_rgb)                                   # 画像をグレースケールで表示
plt.axis("off")                                                   # 軸目盛、軸ラベルを消す
plt.subplot(224)                                                  # 1行2列の2番目の領域にプロットを設定
plt.plot(hist_dst)                                               # ヒストグラムのグラフを表示
plt.xlabel('Brightness')                                          # x軸ラベル(明度)
plt.ylabel('Count')                                               # y軸ラベル(画素の数)
plt.show()



