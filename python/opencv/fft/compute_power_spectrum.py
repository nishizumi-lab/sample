import cv2
import numpy as np
import matplotlib.pyplot as plt

# 画像の読み込み
#img = cv2.imread("C:/github/sample/python/opencv/fft/sample.jpg")
img = cv2.imread("C:/github/sample/python/opencv/fft/lowpass_filter.jpg")

# RGBチャンネルに分割
b, g, r = cv2.split(img)

# パワースペクトルを計算する関数
def compute_power_spectrum(channel):
    # フーリエ変換
    f = np.fft.fft2(channel)
    fshift = np.fft.fftshift(f)
    # パワースペクトル
    power_spectrum = np.abs(fshift) ** 2
    return power_spectrum

# 各チャンネルのパワースペクトルを計算
power_spectrum_r = compute_power_spectrum(r)
power_spectrum_g = compute_power_spectrum(g)
power_spectrum_b = compute_power_spectrum(b)

# パワースペクトルの表示
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(np.log(power_spectrum_r + 1), cmap='gray')
plt.title('Red Channel Power Spectrum')

plt.subplot(1, 3, 2)
plt.imshow(np.log(power_spectrum_g + 1), cmap='gray')
plt.title('Green Channel Power Spectrum')

plt.subplot(1, 3, 3)
plt.imshow(np.log(power_spectrum_b + 1), cmap='gray')
plt.title('Blue Channel Power Spectrum')

plt.show()
