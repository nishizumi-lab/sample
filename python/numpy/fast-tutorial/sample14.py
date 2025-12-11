import numpy as np
import matplotlib.pyplot as plt

# 乱数の種を固定（毎回同じ結果にするため）
np.random.seed(0)

# 100日分の仮想株価を生成（ランダムウォーク）
days = np.arange(100)
price_changes = np.random.normal(loc=0, scale=1, size=100)  # 日ごとの変動
prices = 100 + np.cumsum(price_changes)  # 初期値100から積み上げ

# グラフ描画
plt.figure(figsize=(10, 5))                     # 描画領域（Figure）を作成し、サイズを指定
plt.plot(days, prices, label="Stock Price", color="blue")  # 日数と株価を折れ線グラフとして描画
plt.title("Virtual Stock Price (Random Walk)")  # グラフのタイトルを設定
plt.xlabel("Days")                              # x軸ラベルを設定
plt.ylabel("Price")                             # y軸ラベルを設定
plt.grid(True)                                  # グリッド線を表示
plt.legend()                                    # 凡例（labelで指定した名前）を表示
plt.show()                                      # グラフを画面に表示