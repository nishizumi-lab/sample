import socket
import threading
import cv2

# telloへのアクセス用
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# telloからの受信用
VS_UDP_IP = '0.0.0.0'
VS_UDP_PORT = 11111

# VideoCapture用のオブジェクト準備
cap = None
# データ受信用のオブジェクト準備
response = None

# 通信用のソケットを作成
# ※アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# リッスン状態にする
socket.bind(('', TELLO_PORT))

# データ受け取り用の関数
def run_udp_receiver():
    while True:
        try:
            response, _ = socket.recvfrom(1024)
        except Exception as e:
            print(e)
            break

thread = threading.Thread(target=run_udp_receiver, args=())
thread.daemon = True
thread.start()

# コマンドモードを使うため'command'というテキストを投げる
socket.sendto('command'.encode('utf-8'), TELLO_ADDRESS)

# 離陸
socket.sendto('takeoff'.encode('utf-8'), TELLO_ADDRESS)

# ビデオストリーミング開始
socket.sendto('streamon'.encode('utf-8'), TELLO_ADDRESS)

udp_video_address = 'udp://@' + VS_UDP_IP + ':' + str(VS_UDP_PORT)
if cap is None:
    cap = cv2.VideoCapture(udp_video_address)
if not cap.isOpened():
    cap.open(udp_video_address)
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# ビデオストリーミング停止
socket.sendto('streamoff'.encode('utf-8'), TELLO_ADDRESS)

# 着陸
socket.sendto('land'.encode('utf-8'), TELLO_ADDRESS)