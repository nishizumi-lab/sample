import numpy as np
import matplotlib.pyplot as plt

path = 'C:/github/sample/python/numpy/Stock/sp500/spx_d.csv'

# 日付列だけ文字列として読み込み
dates = np.genfromtxt(path, delimiter=',', skip_header=1, usecols=0, dtype='U10')

# 数値データ（始値〜出来高）を別で読み込み
data = np.genfromtxt(path, delimiter=',', skip_header=1, usecols=(1, 2, 3, 4, 5))

# 終値（4 番目の列：インデックス 3）
close = data[:, 3]

print(dates[:5])
print(close[:5])

plt.figure(figsize=(10, 4))
plt.plot(dates, close, label='S&P500 Close')

plt.title('S&P500 Closing Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)  # 日付ラベルを少し傾けて見やすく
plt.tight_layout()

plt.show()