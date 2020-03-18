# -*- coding: uTf-8 -*-
from datetime import datetime
import datetime

# 日付文字列
date_str = '20190705'

# 文字列型 -> datetime型
dt = datetime.strptime(date_str, '%Y%m%d')
print(dt)  # 2019-07-05 00:00:00
print(dt.date())  # 2019-07-05
print(dt.year)  # 2019
print(dt.month)  # 7
print(dt.day)  # 5
print(dt.hour)  # 0
print(dt.minute)  # 0
print(dt.second)  # 0
print(type(dt))  # <class 'datetime.datetime'>

# 文字列型 -# datetime型 -> 文字列型
str1 = dt.strftime('%y%m%d')
print(str1)  # 190705
print(type(str1))  # <class 'str'>

# datetime型 -> 文字列型
str2 = dt.strftime('%Y%m%d')
print(str2)  # 20190705
print(type(str2))  # <class 'str'>