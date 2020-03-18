import pandas as pd

df1 = pd.DataFrame({'currentA': [10.0, 20.0, 30.0],
                    'voltageA': [100.0, 200.0, 300.0]},
                   index=['2020-01-01', '2020-01-02', '2020-01-03'])

print(df1)
"""
currentA  voltageA
2020-01-01      10.0     100.0
2020-01-02      20.0     200.0
2020-01-03      30.0     300.0
"""

df2 = pd.DataFrame({'currentB': [10.0, 20.0, 30.0],
                    'voltageB': [100.0, 200.0, 300.0]},
                   index=['2020-01-01', '2020-01-02', '2020-01-03'])

print(df2)
"""
currentB  voltageB
2020-01-01      10.0     100.0
2020-01-02      20.0     200.0
2020-01-03      30.0     300.0
"""

df3 = pd.DataFrame({'currentA': [40.0, 50.0, 60.0],
                    'voltageA': [400.0, 500.0, 600.0]},
                   index=['2020-01-04', '2020-01-05', '2020-01-06'])


print(df3)
"""
currentA  voltageA
2020-01-04      40.0     400.0
2020-01-05      50.0     500.0
2020-01-06      60.0     600.0
"""

df_concat = pd.concat([df1, df2], axis=0)
print(df_concat)

"""
            currentA  currentB  voltageA  voltageB 
2020-01-01      10.0       NaN     100.0       NaN 
2020-01-02      20.0       NaN     200.0       NaN 
2020-01-03      30.0       NaN     300.0       NaN 
2020-01-01       NaN      10.0       NaN     100.0 
2020-01-02       NaN      20.0       NaN     200.0 
2020-01-03       NaN      30.0       NaN     300.0 
"""

df_concat = pd.concat([df1, df2], axis=1)
print(df_concat)
"""
            currentA  voltageA  currentB  voltageB 
2020-01-01      10.0     100.0      10.0     100.0 
2020-01-02      20.0     200.0      20.0     200.0 
2020-01-03      30.0     300.0      30.0     300.0 
"""

df_concat = pd.concat([df1, df3], axis=0)
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

df_concat = pd.concat([df1, df3], axis=1)
print(df_concat)
"""
            currentA  voltageA  currentA  voltageA
2020-01-01      10.0     100.0       NaN       NaN 
2020-01-02      20.0     200.0       NaN       NaN 
2020-01-03      30.0     300.0       NaN       NaN 
2020-01-04       NaN       NaN      40.0     400.0 
2020-01-05       NaN       NaN      50.0     500.0 
2020-01-06       NaN       NaN      60.0     600.0 
"""

df_concat = pd.concat([df1, df2, df3], axis=0)
print(df_concat)
"""
            currentA  currentB  voltageA  voltageB 
2020-01-01      10.0       NaN     100.0       NaN 
2020-01-02      20.0       NaN     200.0       NaN 
2020-01-03      30.0       NaN     300.0       NaN 
2020-01-01       NaN      10.0       NaN     100.0 
2020-01-02       NaN      20.0       NaN     200.0 
2020-01-03       NaN      30.0       NaN     300.0 
2020-01-04      40.0       NaN     400.0       NaN 
2020-01-05      50.0       NaN     500.0       NaN 
2020-01-06      60.0       NaN     600.0       NaN
"""

df_concat = pd.concat([df1, df2, df3], axis=0, join='inner')
print(df_concat)
"""
Empty DataFrame
Columns: []
Index: [2020-01-01, 2020-01-02, 2020-01-03, 2020-01-01, 2020-01-02, 2020-01-03, 2020-01-04, 2020-01-05, 2020-01-06]
"""

