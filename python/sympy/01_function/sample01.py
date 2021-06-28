# -*- coding: utf-8 -*-
from sympy import *

# a～zまで変数として扱う
var("a:z")              

# 関数f(x)の定義
f = x**2 + 3*x + 2      

# f(x)=0となるxを計算
ans = solve(Eq(f, 0),x)

print(ans)  # [-2, -1] 