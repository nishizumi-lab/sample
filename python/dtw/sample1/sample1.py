# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from dtw import dtw

x = [1, 2, 3]
y = [1, 3, 4]
SAVE_DIR_PATH = "C:/github/sample/python/dtw/sample1/"

def l2_norm(x, y): return (x - y) ** 2
dist, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=l2_norm)

plt.figure(figsize=(8, 8))
plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.savefig(SAVE_DIR_PATH + "graph.png")
plt.close()

print("dist:", dist)
print("cost_matrix:", cost_matrix)
print("acc_cost_matrix:", acc_cost_matrix)
print("path:", path)

"""
dist: 2.0
cost_matrix:
 [[0. 4. 9.]
 [1. 1. 4.]
 [4. 0. 1.]]

acc_cost_matrix: 
[[ 0.  4. 13.]
 [ 1.  1.  5.]
 [ 5.  1.  2.]]
 
path: (array([0, 1, 2]), array([0, 1, 2]))
"""


