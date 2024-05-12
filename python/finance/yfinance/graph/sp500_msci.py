import yfinance as yf
import datetime as dt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt

# 取得する銘柄コード
stock_code = "^N225" # 日経平均

# 取得するデータの期間
start_date = '2024-04-01'
end_date = '2024-04-17'

# 株価データを取得
df_sp500 = yf.download(tickers=stock_code, start=start_date , end=end_date)

# 取得した株価データを表示
plt.figure(figsize=(30,10))
x = df_sp500.index
y1 = df_sp500['Close']
df_sp500['Close'].plot()
print(df_sp500)
print(x)
print(y1)
#plt.title('S&P500')
#plt.grid(True)
#plt.plot(x,y1,color='b',label='Weekly')
#plt.plot(x,y2,color='r',label='Monthly')
#plt.legend()
#plt.show()
plt.show()