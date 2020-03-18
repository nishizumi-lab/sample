# -*- coding: utf-8 -*-
import pandas as pd

# CSVファイルの読み込み
df = pd.read_csv(
    "C:/github/sample/python/pandas/basic/artoria.csv", index_col=0)

# 合計
sum = df['ATK'].sum()
print("sum:", sum)  # sum:93566

# 平均
mean = df['ATK'].mean()
print("mean:", mean)  # mean:10396.2222222

# 中央値
median = df['ATK'].median()
print("median:", median)  # median: 10995.0

# 最大値
dfmax = df['ATK'].max()
print("max:", dfmax)  # max: 11761

# 最小値
dfmin = df['ATK'].min()
print("min:", dfmin)  # min: 7726

# データ数
N = df['ATK'].count()
print("N:", N)  # N: 9

# 標準偏差
std = df['ATK'].std()
print("std:", std)  # std: 1265.9073601351895

# 分散
var = df['ATK'].var()
print("var:", var)  # var: 1602521.4444444445
