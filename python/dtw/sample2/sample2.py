# -*- coding: utf-8 -*-
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

x = [1, 2, 3]
y = [2, 3, 4]

distance, path = fastdtw(x, y, dist=euclidean)

print("dist:", distance)
print("path:", path)

"""
dist: 2.0
path: [(0, 0), (1, 0), (2, 1), (2, 2)]
"""


