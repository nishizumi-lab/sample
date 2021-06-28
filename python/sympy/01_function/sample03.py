# -*- coding: utf-8 -*-
from sympy import *

# a～zまで変数として扱う
var("a:z")     

# 関数f(x)の定義
f = x**2 + 6*x + 3

# 関数f(x)をxで微分
df = diff(f, x)

print(df) # 2*x + 6

# f'(3)の値を計算
dx = df.subs([(x, 3)])

#計算結果の表示
print(dx) # 12