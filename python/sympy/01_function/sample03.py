# -*- coding: utf-8 -*-
from sympy import *

# a～zまで変数として扱う
var("a:z")     

# 関数f(x)の定義
f = x**2 + 6*x + 3

# 関数f(x)をxで微分
df = diff(f, x)

# x=3のf(x)の傾きを計算
dx = df.subs([(df, 3)])

#計算結果の表示
print(dx) # 3