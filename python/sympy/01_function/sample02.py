# -*- coding: utf-8 -*-
from sympy import *

# a～zまで変数として扱う
var("a:z")

# 関数f(x)の定義          
f = x**2 + 3*x + 2 

# 関数にx=1を代入（f(1)の計算）   
f1 = f.subs([(x, 1)])   

print("f(1)="+str(f1))  # f(1)=6