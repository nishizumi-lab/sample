import pandas as pd  # Pandas を読み込む

# 辞書（dict）形式でサンプルデータを作成
# 3日分の金価格（Open と Close）を用意
data = {
    "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],  # 日付
    "Open": [2000.5, 2003.2, 1998.7],                    # 始値
    "Close": [2001.3, 1999.8, 2005.4],                   # 終値
}

# 辞書データを DataFrame（表形式データ）に変換
df = pd.DataFrame(data)

# DataFrame の内容を表示
print(df)