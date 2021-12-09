import threading 
import socket

# Telloからのレスポンス受信
def recv():
    count = 0
    while True: 
        try:
            # クライアントからのメッセージの受信を受付開始(コネクションレス型)
            data, server = sock.recvfrom(1518)
        except Exception:
            print ('\nExit . . .\n')
            break

host = ""
port = 9000
locaddr = (host,port) 

# UDP通信ソケットの作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Tello側のローカルIPアドレス(デフォルト)、コマンドモード用の宛先ポート番号
tello_address = ('192.168.10.1', 8889)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(locaddr)

# 受信用スレッドの作成
recvThread = threading.Thread(target=recv)
recvThread.start()

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
        sent = sock.sendto(msg, tello_address)

    except KeyboardInterrupt:
        sock.close()  
        break
    
