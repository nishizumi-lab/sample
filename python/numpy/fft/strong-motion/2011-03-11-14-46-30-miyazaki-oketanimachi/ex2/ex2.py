# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# データのパラメータ
N = 36000            # サンプル数
dt = 0.01          # サンプリング間隔
fc1 = 0.5  # カットオフ周波数1[Hz]
fc2 = 35.0  # カットオフ周波数2[Hz]
A1, A2 = 20, 5
t = np.arange(0, N*dt, dt)  # 時間軸
freq = np.linspace(0, 1.0/dt, N)  # 周波数軸
hamm = np.hamming(N)  # ハミング窓

# CSVのロード
df = pd.read_csv("C:/github/sample/python/numpy/fft/strong-motion/2011-03-11-14-46-30-miyazaki-oketanimachi/ex2/data.csv",
                 encoding="UTF-8", skiprows=6)

# 3列目(UD)のデータ（加速度）終値だけを取り出し

f = df["UD"]
# 高速フーリエ変換（周波数信号に変換）
F = np.fft.fft(f*hamm)

# 正規化 + 交流成分2倍
F = F / (N / 2)

# 直流成分は等倍に戻す
F[0] = F[0]/2

# 配列Fをコピー
F2 = F.copy()

# バンドパスフィルタ処理（fc1～fc2[Hz]の帯域以外を0にする）
F2[(freq > fc2)] = 0
F2[(freq < fc1)] = 0

# 高速逆フーリエ変換（時間信号に戻す）
f2 = np.fft.ifft(F2)

# 振幅を元のスケールに戻す
f2 = np.real(f2*N)

# 周波数軸のデータを保存
spectrum_df = pd.DataFrame({})
spectrum_df["freq"] = freq
spectrum_df.set_index("freq", inplace=True)
spectrum_df["F1"] = np.abs(F)
spectrum_df["F2"] = np.abs(F2)
spectrum_df.to_csv(
    "C:/github/sample/python/numpy/fft/strong-motion/2011-03-11-14-46-30-miyazaki-oketanimachi/ex2/spectrum_" + str(fc1) + "_" + str(fc2) + ".csv")

# 時間軸のデータを保存
amplitude_df = pd.DataFrame({})
amplitude_df["time"] = t
#amplitude_df.set_index("time", inplace=True)
amplitude_df["f"] = f
amplitude_df["f2"] = f2
amplitude_df.to_csv(
    "C:/github/sample/python/numpy/fft/strong-motion/2011-03-11-14-46-30-miyazaki-oketanimachi/ex2/amplitude_" + str(fc1) + "_" + str(fc2) + ".csv")


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
plt.savefig(
    "C:/github/sample/python/numpy/fft/strong-motion/2011-03-11-14-46-30-miyazaki-oketanimachi/ex2/" + str(fc1) + "_" + str(fc2) + ".png")
