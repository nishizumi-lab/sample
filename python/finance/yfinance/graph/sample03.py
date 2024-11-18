import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# オルカン（All Country World Index）のティッカーシンボル
acwi_ticker = "ACWI"

# S&P 500のティッカーシンボル
sp500_ticker = "^GSPC"

# 過去5年間の株価データを取得
acwi_data = yf.download(acwi_ticker, start="2019-11-01", end="2024-11-01")
sp500_data = yf.download(sp500_ticker, start="2019-11-01", end="2024-11-01")

# 株価データの終値を取得
acwi_close = acwi_data["Close"].values.reshape(-1, 1)
sp500_close = sp500_data["Close"].values.reshape(-1, 1)

# 正規化
scaler = MinMaxScaler()
acwi_normalized = scaler.fit_transform(acwi_close)
sp500_normalized = scaler.fit_transform(sp500_close)

# グラフの作成
plt.figure(figsize=(14, 7))
plt.plot(acwi_data.index, acwi_normalized, label="ACWI")
plt.plot(sp500_data.index, sp500_normalized, label="S&P 500")
plt.title("ACWI vs S&P 500 - Past 5 Years (Normalized)")
plt.xlabel("Date")
plt.ylabel("Normalized Price (0-1)")
plt.legend()
plt.grid(True)
plt.show()
