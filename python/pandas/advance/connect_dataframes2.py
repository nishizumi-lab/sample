import pandas as pd

list_df = []


list_df.append(pd.DataFrame({'currentA': [10.0, 20.0, 30.0],
                    'voltageA': [100.0, 200.0, 300.0]},
                   index=['2020-01-01', '2020-01-02', '2020-01-03']))

print(list_df[0])
"""
            currentA  voltageA
2020-01-01      10.0     100.0
2020-01-02      20.0     200.0
2020-01-03      30.0     300.0
"""

list_df.append(pd.DataFrame({'currentA': [40.0, 50.0, 60.0],
                    'voltageA': [400.0, 500.0, 600.0]},
                   index=['2020-01-04', '2020-01-05', '2020-01-06']))

print(list_df[1])
"""
            currentA  voltageA
2020-01-04      40.0     400.0
2020-01-05      50.0     500.0
2020-01-06      60.0     600.0
"""

# 連結
df_concat = pd.concat(list_df)
print(df_concat)
"""
            currentA  voltageA
2020-01-01      10.0     100.0
2020-01-02      20.0     200.0
2020-01-03      30.0     300.0
2020-01-04      40.0     400.0
2020-01-05      50.0     500.0
2020-01-06      60.0     600.0
"""
