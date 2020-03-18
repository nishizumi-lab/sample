# -*- coding: utf-8 -*-
import pandas as pd

new_dict1 = {'key1': [11, 12], 'key2': [21, 22], 'key3': [31]}
df1 = pd.DataFrame.from_dict(new_dict1, orient='index').T
print(df1)
"""
   key1  key2  key3
0  11.0  21.0  31.0
1  12.0  22.0   NaN
"""

new_dict2 = {}
list_key1 = [11, 12]
list_key2 = [21, 22]
list_key3 = [31]
new_dict2["key1"] = list_key1
new_dict2["key2"] = list_key2
new_dict2["key3"] = list_key3
df2 = pd.DataFrame.from_dict(new_dict2, orient='index').T
print(df2)
"""
   key1  key2  key3
0  11.0  21.0  31.0
1  12.0  22.0   NaN
"""
