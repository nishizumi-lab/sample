import numpy as np

# 5日分の株価データ（例）
prices = np.array([100, 102, 98, 105, 110])

# マスク用の配列を生成（True の日だけ抽出）
mask = np.array([True, False, False, True, False])

# True の要素のみ取り出し
selected = prices[mask]
print(selected)  # [100 105]

# True の要素のみ値を代入（例：特定日の株価を補正）
prices[mask] = 999
print(prices)  # [999 102  98 999 110]

# マスク用の配列を生成（900以上だけ抽出）
print(prices >= 900) # [ True False False  True False]

# 900以上の要素を0にする
prices[prices >= 900] = 0
print(prices)  # [  0 102  98   0 110]