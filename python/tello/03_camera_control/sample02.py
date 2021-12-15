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
                    time_text = "Time:" + resp + "s"
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
        print("-----")
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
# 上昇(20cm)
def up():
        try:
            sent = sock.sendto('up 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 下降(20cm)
def down():
        try:
            sent = sock.sendto('down 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 前に進む(20cm)
def forward():
        try:
            sent = sock.sendto('forward 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 後に進む(20cm)
def back():
        try:
            sent = sock.sendto('back 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右に進む(20cm)
def right():
        try:
            sent = sock.sendto('right 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左に進む(20cm)
def left():
        try:
            sent = sock.sendto('left 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 右回りに回転(90 deg)
def cw():
        try:
            sent = sock.sendto('cw 90'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 左回りに回転(90 deg)
def ccw():
        try:
            sent = sock.sendto('ccw 90'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 高速モード(速度40cm/sec)
def speed40():
        try:
            sent = sock.sendto('speed 40'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass
# 低速モード(速度20cm/sec)
def speed20():
        try:
            sent = sock.sendto('speed 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
        except:
            pass

# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# Telloからの映像受信用のローカルIPアドレス、宛先ポート番号
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111'

command_text = "WAIT..."
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

while True:
    ret, frame = cap.read()

    # 動画フレームが空ならスキップ
    if frame is None or frame.size == 0:
        continue

    # カメラ映像のサイズを半分にしてウィンドウに表示
    frame_height, frame_width = frame.shape[:2]
    frame2 = cv2.resize(frame, (int(frame_width/2), int(frame_height/2)))
    
    # 送信したコマンドを表示
    cv2.putText(frame2,
            text=command_text,
            org=(10, 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)

    cv2.putText(frame2,
            text=battery_text,
            org=(10, 40),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)

    cv2.putText(frame2,
            text=time_text,
            org=(10, 60),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)

    cv2.putText(frame2,
            text=status_text,
            org=(10, 80),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)

    cv2.imshow('Tello Camera View', frame2)
    key = cv2.waitKey(1)
    # qキーで終了
    if key == ord('q'):
        break
    elif key == 2490368:
        up()
        command_text = "UP"
    elif key == 2621440:
        down()
        command_text = "DOWN"
    elif key == 2424832:
        left()
        command_text = "LEFT"
    elif key == 2555904:
        right()
        command_text = "RIGHT"
    elif key == ord('j'):
        takeoff()
        command_text = "TAKE OFF"
    elif key == ord('k'):
        land()
        command_text = "LAND"
    elif key == ord('h'):
        ccw()
        command_text = "CCW"
    elif key == ord('l'):
        cw()
        command_text = "CW"

cap.release()
cv2.destroyAllWindows()

# ビデオストリーミング停止
sock.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)
