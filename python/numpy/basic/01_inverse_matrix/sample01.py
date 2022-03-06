import numpy as np

def calc_invA(A):
    n = len(A)
    I = np.eye(n).astype(np.float64)
     # 操作中の行がy
    for y in range(n):  
        max = abs(A[y, y])
        indx = y
        for yy in range(y + 1, n):
            if max < abs(A[yy, y]):
                max = abs(A[yy, y])
                indx = yy
        if indx != y:
            for x in range(n):
                tmp = A[indx, x]
                A[indx, x] = A[y, x]
                A[y, x] = tmp
                tmp = I[indx, x]
                I[indx, x] = I[y, x]
                I[y, x] = tmp
         # 対角成分
        gain = 1/A[y, y]    
        for x in range(n):
            # 対角成分を1へ
            A[y, x] = A[y, x] * gain    
            I[y, x] = I[y, x] * gain
        # 操作される行（消される行）
        for yy in range(n): 
            # 自分自身の行でないときに
            if y != yy: 
                # 対角成分
                gain = A[yy, y] 
                for x in range(n):
                    A[yy, x] = A[yy, x] - A[y, x] * gain
                    I[yy, x] = I[yy, x] - I[y, x] * gain
    return I

A = [[1, 1, 0],[0, 1, 1],[0, 1, 0]]
A = np.array(A)

print(np.linalg.inv(A))
"""
[[ 1.  0. -1.]
 [ 0.  0.  1.]
 [-0.  1. -1.]]
"""

invA = calc_invA(A)
print(invA)
"""
[[ 1.  0. -1.]
 [ 0.  0.  1.]
 [-0.  1. -1.]]
"""


A = [[2, 1, 2],[3, 1, 4],[2, 1, 5]]
A = np.array(A)

print(np.linalg.inv(A))
"""
[[-0.33333333  1.         -0.66666667]
 [ 2.33333333 -2.          0.66666667]
 [-0.33333333  0.          0.33333333]]
"""

invA = calc_invA(A)
print(invA)
"""
[[ 0.33333333  0.33333333 -0.33333333]
 [ 1.         -0.66666667  0.        ]
 [-0.33333333  0.          0.33333333]]
"""