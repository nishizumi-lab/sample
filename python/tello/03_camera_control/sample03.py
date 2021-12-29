import socket
import threading
import cv2
import time
import numpy as np


# データ受け取り用の関数
def udp_receiver():
        global battery_text
        global time_text
        global status_text

        while True: 
            try:
                data, server = sock.recvfrom(1518)
                resp = data.decode(encoding="utf-8").strip()
                # レスポンスが数字だけならバッテリー残量
                if resp.isdecimal():    
                    battery_text = "Battery:" + resp + "%"
                # 最後の文字がsなら飛行時間
                elif resp[-1:] == "s":
                    time_text = "Time:" + resp
                else: 
                    status_text = "Status:" + resp
            except:
                pass

# 問い合わせ
def ask():
    while True:
        try:
            sent = sock.sendto('battery?'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
        time.sleep(0.5)

        try:
            sent = sock.sendto('time?'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
        time.sleep(0.5)


# 離陸
def takeoff():
        try:
            sent = sock.sendto('takeoff'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 着陸
def land():
        try:
            sent = sock.sendto('land'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 上昇(cm)
def up(distance):
        try:
            sent = sock.sendto('up ' + str(distance).encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 下降(cm)
def down(distance):
        try:
            sent = sock.sendto('down ' + str(distance).encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 前に進む(cm)
def forward(distance):
        try:
            sent = sock.sendto('forward ' + str(distance).encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 後に進む(cm)
def back(distance):
        try:
            sent = sock.sendto('back ' + str(distance).encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右に進む(20cm)
def right(distance):
        try:
            sent = sock.sendto('right ' + str(distance).encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左に進む(20cm)
def left(distance):
        try:
            sent = sock.sendto('left ' + str(distance).encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右回りに回転(90 deg)
def cw(distance):
        try:
            sent = sock.sendto('cw ' + str(distance).encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左回りに回転(90 deg)
def ccw():
        try:
            sent = sock.sendto('ccw 90'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass


# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# Telloからの映像受信用のローカルIPアドレス、宛先ポート番号
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111'

command_text = "None"
battery_text = "Battery:"
time_text = "Time:"
status_text = "Status:"

# キャプチャ用のオブジェクト
cap = None

# データ受信用のオブジェクト備
response = None

# 通信用のソケットを作成
# ※アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))

# 問い合わせスレッド起動
ask_thread = threading.Thread(target=ask)
ask_thread.setDaemon(True)
ask_thread.start()

# 受信用スレッドの作成
recv_thread = threading.Thread(target=udp_receiver, args=())
recv_thread.daemon = True
recv_thread.start()

# コマンドモード
sock.sendto('command'.encode('utf-8'), TELLO_ADDRESS)

time.sleep(1)

# カメラ映像のストリーミング開始
sock.sendto('streamon'.encode('utf-8'), TELLO_ADDRESS)

time.sleep(1)

if cap is None:
    cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)

if not cap.isOpened():
    cap.open(TELLO_CAMERA_ADDRESS)

time.sleep(1)

# カスケード型識別器の読み込み
cascade = cv2.CascadeClassifier("./lbpcascade_animeface.xml")

while True:
    ret, frame = cap.read()

    # 動画フレームが空ならスキップ
    if frame is None or frame.size == 0:
        continue

    # カメラ映像のサイズを半分にしてウィンドウに表示
    frame_height, frame_width = frame.shape[:2]
    frame2 = cv2.resize(frame, (int(frame_width/2), int(frame_height/2)))

    # グレースケール変換
    gray_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # アニメ顔領域の探索
    faces = cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
    
    # もしアニメ顔が1つ以上あれば
    if len(faces) > 0:
        # 最も大きいアニメ顔の座標のみ抽出
        max_face = max(faces, key=lambda x: x[2] * x[3])
        # 顔領域を赤色の矩形で囲む
        for (face_x, face_y, face_w, face_h) in max_face:
            cv2.rectangle(gray_frame, (face_x, face_y), (face_x + face_w, face_y+face_h), (0, 0, 200), 3)
    
        # アニメ顔の中心座標を取得
        face_center_x = int(face_x + face_w/2)
        face_center_y = int(face_y + face_h/2)
        face_area = int(face_w * face_h)
        
        # オブジェクトが画像の左側に位置していたら、反時計回りに旋回する
        if face_center_x < face_w / 2 - 100:
            ccw()
            command_text = "Ccw"
        # オブジェクトが画像の右側に位置していたら、時計回りに旋回する
        elif face_center_x > face_w / 2 + 100:
            cw()
            command_text = "Cw"
        # オブジェクトが画像の上側に位置していたら、上昇する
        elif face_center_y < face_h / 2 - 50:
            up()
            command_text = "Up"
        # オブジェクトが画像の下側に位置していたら、下降する
        elif face_center_y > face_h / 2 + 50:
            down()
            command_text = "Down"
        # オブジェクトの面積が小さい場合、前進する
        elif face_area < 200000:
            forward()
            command_text = "Forward"
        elif face_area < 200000:
            back()
            command_text = "Back"

    # 送信したコマンドを表示
    cv2.putText(frame2,
            text="Cmd:" + command_text,
            org=(10, 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    # バッテリー残量を表示
    cv2.putText(frame2,
            text=battery_text,
            org=(10, 40),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    # 飛行時間を表示
    cv2.putText(frame2,
            text=time_text,
            org=(10, 60),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)
    # ステータスを表示
    cv2.putText(frame2,
            text=status_text,
            org=(10, 80),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=1,
            lineType=cv2.LINE_4)

    # カメラ映像を画面に表示
    cv2.imshow('Tello Camera View', frame2)

    # キー入力を取得
    key = cv2.waitKey(1)

    # qキーで終了
    if key == ord('q'):
        takeoff()
        break
    # ↑キーで前進
    elif key == 2490368:
        forward()
        command_text = "Forward"
    # ↓キーで後進
    elif key == 2621440:
        back()
        command_text = "Back"
    # ←キーで左進
    elif key == 2424832:
        left()
        command_text = "Left"
    # →キーで右進
    elif key == 2555904:
        right()
        command_text = "Right"
    # jキーで離陸
    elif key == ord('j'):
        takeoff()
        command_text = "Take off"
    # kキーで着陸
    elif key == ord('k'):
        land()
        command_text = "Land"
    # hキーで上昇
    elif key == ord('h'):
        up()
        command_text = "Up"
    # lキーで下降
    elif key == ord('l'):
        down()
        command_text = "Down"
    # uキーで左回りに回転
    elif key == ord('u'):
        ccw()
        command_text = "Ccw"
    # iキーで右回りに回転
    elif key == ord('i'):
        cw()
        command_text = "Cw"



cap.release()
cv2.destroyAllWindows()

# ビデオストリーミング停止
sock.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)
