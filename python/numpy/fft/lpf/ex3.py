# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# データのパラメータ
N = 256            # サンプル数
dt = 0.01          # サンプリング間隔
fq1, fq2 = 5, 20    # 周波数
fc = 10            # カットオフ周波数
t = np.arange(0, N*dt, dt)  # 時間軸
freq = np.linspace(0, 1.0/dt, N)  # 周波数軸

#t = np.linspace(0, 1, N, endpoint=False)
f1 = signal.square(2 * np.pi * fq1 * t)
f2 = 0.2 * signal.square(2 * np.pi * fq2 * t)
f = f1 + f2

# 高速フーリエ変換（周波数信号に変換）
F = np.fft.fft(f)

# 正規化 + 交流成分2倍
F = F/(N/2)
F[0] = F[0]/2

# 配列Fをコピー
F2 = F.copy()

# ローパスフィル処理（カットオフ周波数を超える帯域の周波数信号を0にする）
F2[(freq > fc)] = 0

# 高速逆フーリエ変換（時間信号に戻す）
f2 = np.fft.ifft(F2)

# 振幅を元のスケールに戻す
f2 = np.real(f2*N)

# グラフ表示

fig = plt.figure(figsize=(10.0, 8.0))
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# 時間信号（元）
plt.subplot(221)
plt.plot(t, f, label='f(n)')
plt.xlabel("Time", fontsize=12)
plt.ylabel("Signal", fontsize=12)
plt.grid()
leg = plt.legend(loc=1, fontsize=15)
leg.get_frame().set_alpha(1)

# 周波数信号(元)
plt.subplot(222)
plt.plot(freq, np.abs(F), label='|F(k)|')
plt.xlabel('Frequency', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.grid()
leg = plt.legend(loc=1, fontsize=15)
leg.get_frame().set_alpha(1)

# 時間信号(処理後)
plt.subplot(223)
plt.plot(t, f2, label='f2(n)')
plt.xlabel("Time", fontsize=12)
plt.ylabel("Signal", fontsize=12)
plt.grid()
leg = plt.legend(loc=1, fontsize=15)
leg.get_frame().set_alpha(1)

# 周波数信号(処理後)
plt.subplot(224)
plt.plot(freq, np.abs(F2), label='|F2(k)|')
plt.xlabel('Frequency', fontsize=12)
plt.ylabel('Amplitude', fontsize=12)
plt.grid()
leg = plt.legend(loc=1, fontsize=15)
leg.get_frame().set_alpha(1)
plt.savefig('C:/github/sample/python/numpy/fft/lpf/ex3.png')
