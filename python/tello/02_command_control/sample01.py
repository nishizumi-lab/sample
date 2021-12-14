import threading 
import socket


# Telloからのレスポンス受信
def udp_receiver():
    count = 0
    while True: 
        try:
            # クライアントからのメッセージの受信を受付開始(コネクションレス型)
            data, server = sock.recvfrom(1518)
        except Exception:
            print ('\nExit . . .\n')
            break

# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# UDP通信ソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))

# 受信用スレッドの作成
thread  = threading.Thread(target=udp_receiver)
thread.daemon = True
thread .start()

while True: 

    try:
        msg = input("")

        # メッセージがなければ何もしない
        if not msg:
            break  

        # 「q」でソケット通信終了
        if 'q' in msg:
            print ('QUIT...')
            sock.close()  
            break

        # データを送信
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, TELLO_ADDRESS)

    except KeyboardInterrupt:
        sock.close()  
        break
    
