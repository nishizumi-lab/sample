# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# (x1, y1)のデータセットを作成
x1 = np.arange(-3.14, 3.14, 0.25)
y1 = np.sin(x1)

# (x2, y2)のデータセットを作成
x2 = np.linspace(0, 3, 10)  # xの値域：0-3、10分割
y2 = x2 + 1               # 直線の式

# プロット
plt.plot(x1, y1, "r-",lw=2, alpha=0.7, ms=2,label="(x1, y1)") # 線プロット
plt.plot(x2, y2, "bo",lw=2, alpha=0.7, ms=5,label="(x2, y2)") # 点プロット

# グラフ設定
plt.rcParams['font.family'] = 'Times New Roman' # 全体のフォント
plt.rcParams['font.size'] = 20                  # フォントサイズ
plt.rcParams['axes.linewidth'] = 1.0    # 軸の太さ 
plt.legend(loc=2,fontsize=20)           # 凡例の表示（2：位置は第二象限）
plt.title('Graph Title', fontsize=20)   # グラフタイトル
plt.xlabel('x', fontsize=20)            # x軸ラベル
plt.ylabel('y', fontsize=20)            # y軸ラベル
plt.xlim([-3, 3])                       # x軸範囲
plt.ylim([-2, 4])                       # y軸範囲
plt.tick_params(labelsize = 20)         # 軸ラベルの目盛りサイズ
plt.xticks(np.arange(-3.0, 4.0, 1.0))   # x軸の目盛りを引く場所を指定（無ければ自動で決まる）
plt.yticks(np.arange(-3.0, 4.0, 1.0))   # y軸の目盛りを引く場所を指定（無ければ自動で決まる）
plt.axis('scaled')                      # x, y軸のスケールを均等
plt.tight_layout()                      # ラベルがきれいに収まるよう表示
plt.grid()                              # グリッドの表示
plt.show()                              # グラフ表示