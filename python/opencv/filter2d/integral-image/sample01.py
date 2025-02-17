import cv2 as cv
import numpy as np

# サンプルのグレースケール画像データを作成（5x5の行列）
gray = np.array([[0, 0, 0, 0, 0],
                 [0, 1, 1, 1, 0],
                 [0, 1, 1, 1, 0],
                 [0, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0]], dtype=np.uint8)


# 積分画像の作成
integral = cv.integral(gray)

# 積分画像を表示
print("integral=\n", integral)

'''
実行結果

integral=
 [[0 0 0 0 0 0]
  [0 0 0 0 0 0]
  [0 0 1 2 3 3]
  [0 0 2 4 6 6]
  [0 0 3 6 9 9]
  [0 0 3 6 9 9]]
 '''