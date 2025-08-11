import cv2

# SIFTオブジェクトを作成
sift = cv2.SIFT_create()

# 特徴点と記述子を検出
keypoints, descriptors = sift.detectAndCompute(image, None)

# 結果の描画
output = cv2.drawKeypoints(image, keypoints, None)