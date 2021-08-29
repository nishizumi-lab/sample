# -*- coding: utf-8 -*-
from sklearn import datasets

# 糖尿病患者のデータセットをロード
dataset = datasets.load_diabetes()

print(dataset)

"""
{'data': array([[ 0.03807591,  0.05068012,  0.06169621, ..., -0.00259226,
         0.01990842, -0.01764613],
         ....
        'target': array([151.,  75., 141., 206., 135.,  97., 138.,  63., 110., 310., 101.,
        ....
"""