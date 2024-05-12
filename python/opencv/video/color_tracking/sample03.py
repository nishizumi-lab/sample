# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time

def red_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0,127,0])
    hsv_max = np.array([30,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150,127,0])
    hsv_max = np.array([179,255,255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)
    
    return mask1 + mask2

# ブロブ解析
def analysis_blob(binary_img):
    # 2値画像のラベリング処理
    label = cv2.connectedComponentsWithStats(binary_img)

    # ブロブ情報を項目別に抽出
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)

    # ブロブ面積最大のインデックス
    max_index = np.argmax(data[:, 4])

    # 面積最大ブロブの情報格納用
    maxblob = {}

    # 面積最大ブロブの各種情報を取得
    maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
    maxblob["width"] = data[:, 2][max_index]  # 幅
    maxblob["height"] = data[:, 3][max_index]  # 高さ
    maxblob["area"] = data[:, 4][max_index]   # 面積
    maxblob["center"] = center[max_index]  # 中心座標
    
    return maxblob


def main():
    # データ格納用のリスト
    data = []

    # 動画ファイルのパス
    videofile_path = "C:/github/sample/python/opencv/video/color_tracking/red_pendulum.mp4"

    # 記録データの保存先パス
    csvfile_path = "C:/github/sample/python/opencv/video/color_tracking/data.csv"

    # カメラのキャプチャ
    cap = cv2.VideoCapture(videofile_path)

    # 開始時間
    start = time.time()

    while(cap.isOpened()):
        # フレームを取得
        ret, frame = cap.read()

        # カラートラッキング（赤色）
        mask = red_detect(frame)

        # マスク画像をブロブ解析（面積最大のブロブ情報を取得）
        target = analysis_blob(mask)

        # 面積最大ブロブの中心座標を取得
        center_x = int(target["center"][0])
        center_y = int(target["center"][1])

        # フレームに面積最大ブロブの中心周囲を円で描く
        cv2.circle(frame, (center_x, center_y), 30, (0, 200, 0),
                   thickness=3, lineType=cv2.LINE_AA)

        # 経過時間, x, yをリストに追加
        data.append([time.time() - start, center_x, center_y])

        # ウィンドウ表示
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # CSVファイルに保存
    np.savetxt(csvfile_path, np.array(data), delimiter=",")

    # キャプチャ解放・ウィンドウ廃棄
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
