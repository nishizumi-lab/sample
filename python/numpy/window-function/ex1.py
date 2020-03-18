# -*- coding: utf-8 -*-
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


N = 512            # サンプル数
dt = 0.01          # サンプリング間隔
t = np.arange(0, N * dt, dt)  # 時間軸

# 窓関数の一例
fw1 = np.hanning(N)             # ハニング窓
fw2 = np.hamming(N)          # ハミング窓
fw3 = np.blackman(N)         # ブラックマン窓

# グラフ表示
fig = plt.figure(figsize=(7.0, 5.0))
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# 時間信号（元）
plt.plot(t, fw1, label='hann')
plt.plot(t, fw2, label='hamming')
plt.plot(t, fw3, label='blackman')
plt.xlabel("Time", fontsize=12)
plt.ylabel("Amplitude", fontsize=12)
plt.grid()
leg = plt.legend(loc=1, fontsize=15)

plt.savefig('C:/github/sample/python/scipy/window-function/ex1.png')
