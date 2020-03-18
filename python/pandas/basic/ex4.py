# -*- coding: utf-8 -*-
import pandas as pd

# 日時のインデックス作成
date = pd.date_range("20170201", periods=21)

# 表示
print(date)

"""
class 'pandas.tseries.index.DatetimeIndex'
[2017-02-01 00:00:00, ..., 2017-02-21 00:00:00]
Length: 21, Freq: D, Timezone: None
"""