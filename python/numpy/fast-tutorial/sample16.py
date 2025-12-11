import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Stooq が提供しているゴールド価格（XAUUSD）のCSVデータを読み込む
# ゴールド価格の過去から現在までの終値や始値が日ごとに記録されている
url = "https://stooq.com/q/d/l/?s=xauusd&i=d"
df = pd.read_csv(url)

# "Date" 列を文字列（str）から日付（datetime）型に変換する
# こうすることで、「日付として」並べ替えたり、期間で絞り込んだりできるようになる
df["Date"] = pd.to_datetime(df["Date"])

# 日付が古い順（昇順）になるように並べ替える
# Stooq のデータは新しい日付が上に来るため、このままだとグラフが逆向きになってしまう
df = df.sort_values("Date")

# 今日から1年前の日付を計算する
# timedelta(days=365) は「365日前」を表すオブジェクト
one_year_ago = datetime.now() - timedelta(days=365)

# データフレームから「直近1年分だけ」を取り出す
# 条件式 df["Date"] >= one_year_ago を満たす行だけを残している
df_recent = df[df["Date"] >= one_year_ago]

# ============================
# 1. 基本統計量の表示
# ============================

# 「Close（終値）」列について、平均・標準偏差・最小値・最大値などの基本統計量を計算して表示する
# これにより、「この1年でどのくらいの価格帯で動いていたのか」がざっくり把握できる
print("▼ 直近1年の基本統計量")
print(df_recent["Close"].describe())

# ============================
# 2. 年初来リターン（最初の終値 → 最新の終値）
# ============================

# 直近1年のうち、最初の日の終値（スタートの価格）を取り出す
start_price = df_recent["Close"].iloc[0]

# 直近1年のうち、最後の日の終値（最新の価格）を取り出す
end_price = df_recent["Close"].iloc[-1]

# リターン（変化率）を計算する
# （最新価格 - 最初の価格） ÷ 最初の価格 × 100（％表示のため）
return_rate = (end_price - start_price) / start_price * 100

print("\n▼ 年初来リターン")
print(f"{return_rate:.2f}%")  # 小数点以下2桁まで表示

# ============================
# 3. 移動平均線（SMA）を追加
# ============================

# 「20日移動平均」を計算する
# 直近20日間の終値の平均を、1日ずつずらしながら計算していく
df_recent["SMA_20"] = df_recent["Close"].rolling(window=20).mean()  # 20日移動平均

# 「60日移動平均」を計算する（より長い期間のトレンドを見る指標）
df_recent["SMA_60"] = df_recent["Close"].rolling(window=60).mean()  # 60日移動平均

# ============================
# グラフ描画
# ============================

# グラフ全体のサイズを指定（横12インチ × 縦5インチ）
plt.figure(figsize=(12, 5))

# 終値の折れ線グラフを描画（横軸に日付、縦軸に終値Closeを使う）
plt.plot(df_recent["Date"], df_recent["Close"], label="Close", color="gold")

# 20日移動平均線を青色で描画
plt.plot(df_recent["Date"], df_recent["SMA_20"], label="SMA 20", color="blue", alpha=0.7)

# 60日移動平均線を赤色で描画
plt.plot(df_recent["Date"], df_recent["SMA_60"], label="SMA 60", color="red", alpha=0.7)

plt.title("Gold Price Trend (Stooq XAUUSD) - Last 1 Year") # グラフのタイトル
plt.xlabel("Date") # 横軸（x軸）のラベル
plt.ylabel("Price (USD)") # 縦軸（y軸）のラベル
plt.grid(True) # 背景にグリッド（目盛りの補助線）を表示
plt.legend() # 凡例
plt.show() # グラフを画面に表示