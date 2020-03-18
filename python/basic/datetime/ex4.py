# -*- coding: uTf-8 -*-
from datetime import datetime

# 日付文字列
date_str = '2019-07-05 12:34:56'

# 文字列型 -> datetime型
dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
print(dt)  # 2019-07-05 12:34:56
print(dt.date())  # 2019-07-05
print(dt.year)  # 2019
print(dt.month)  # 7
print(dt.day)  # 5
print(dt.hour)  # 12
print(dt.minute)  # 34
print(dt.second)  # 56
print(type(dt))  # <class 'datetime.datetime'>

# datetime型 -> 文字列型
str1 = dt.strftime('%y%m%d')
print(str1)  # 190705
print(type(str1))  # <class 'str'>

# datetime型 -> 文字列型
str2 = dt.strftime('%Y%m%d')
print(str2)  # 20190705
print(type(str2))  # <class 'str'>
