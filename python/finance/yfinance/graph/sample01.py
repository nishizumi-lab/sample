import yfinance as yf
import matplotlib.pyplot as plt

# オルカン（All Country World Index）のティッカーシンボル
acwi_ticker = "ACWI"

# S&P 500のティッカーシンボル
sp500_ticker = "^GSPC"

# 過去5年間の株価データを取得
acwi_data = yf.download(acwi_ticker, start="2019-11-01", end="2024-11-01")
sp500_data = yf.download(sp500_ticker, start="2019-11-01", end="2024-11-01")

# 株価データの終値を取得
acwi_close = acwi_data["Close"]
sp500_close = sp500_data["Close"]


# グラフの作成
plt.figure(figsize=(14, 7))
plt.plot(acwi_close, label="ACWI")
plt.plot(sp500_close, label="S&P 500")
plt.title("ACWI vs S&P 500 - Past 5 Years")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.legend()
plt.grid(True)
plt.show()