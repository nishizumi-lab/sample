# -*- coding: utf-8 -*-
import pandas as pd

def count_continuous_values(df, column_name):
    y = df[column_name]
    df[column_name+ "_counum"] = y.groupby((y != y.shift()).cumsum()).cumcount() + 1

    return df

df = pd.DataFrame({'voltage' : [0.0,0.1,1.0,1.0,4.0,2.0,2]} )

count_continuous_values(df, "voltage")

print(df)
"""
   voltage  voltage_counum
0      0.0               1
1      0.1               1
2      1.0               1
3      1.0               2
4      4.0               1
5      2.0               1
6      2.0               2
"""
