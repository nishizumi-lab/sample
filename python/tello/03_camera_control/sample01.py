import socket
import threading
import cv2
import numpy as np

# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# Telloからの映像受信用のローカルIPアドレス、宛先ポート番号
VS_UDP_IP = '0.0.0.0'
VS_UDP_PORT = 11111

# データ受信用のオブジェクト準備
response = None

# UDP通信ソケットの作成(アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))

# データ受け取り用の関数
def udp_receiver():
    while True:
        try:
            # クライアントからのメッセージの受信を受付開始(コネクションレス型)
            response, _ = socket.recvfrom(1024)
        except Exception as e:
            print(e)
            break

# 受信用スレッドの作成
thread = threading.Thread(target=udp_receiver, args=())
thread.daemon = True
thread.start()

# カメラ映像のストリーミング開始
sock.sendto('streamon'.encode('utf-8'), TELLO_ADDRESS)

tello_camera_address = 'udp://@' + VS_UDP_IP + ':' + str(VS_UDP_PORT)

cap = cv2.VideoCapture(tello_camera_address)

if not cap.isOpened():
    cap.open(tello_camera_address)

while True:
    ret, frame = cap.read()

    # カメラ映像のサイズを半分にしてウィンドウに表示
    frame_height, frame_width = frame.shape[:2]
    frame2 = cv2.resize(frame, (frame_height / 2, frame_width / 2))
    cv2.imshow('Tello Camera View', frame2)

    # qキーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # カメラ映像のストリーミング停止
        sock.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)
        break

cap.release()
cv2.destroyAllWindows()