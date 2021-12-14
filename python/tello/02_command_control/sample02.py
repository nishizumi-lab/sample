# -*- coding: utf-8 -*-
import threading 
import socket
import tkinter as tk
import time

# Tello側のローカルIPアドレス(デフォルト)、宛先ポート番号(コマンドモード用)
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

# UDP通信ソケットの作成(アドレスファミリ：AF_INET（IPv4）、ソケットタイプ：SOCK_DGRAM（UDP）)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 自ホストで使用するIPアドレスとポート番号を設定
sock.bind(('', TELLO_PORT))


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

# Telloからのレスポンス受信
def udp_receiver():
        while True: 
            try:
                data, server = sock.recvfrom(1518)
                resp = data.decode(encoding="utf-8").strip()
                # レスポンスが数字だけならバッテリー残量
                if resp.isdecimal():    
                    battery_text.set("電池残量:" + resp + "%")
                # 最後の文字がsなら飛行時間
                elif resp[-1:] == "s":
                    time_text.set("飛行時間:" + resp + "秒")
                else: 
                    status_text.set("ステータス:" + resp)
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

# 画面作成
root = tk.Tk()
root.geometry('300x600')
root.title('ボタンイベントの検証')

# 最初にcommandコマンドを送信
try:
    sent = sock.sendto('command'.encode(encoding="utf-8"), TELLO_ADDRESS)
except:
    pass
# 速度を遅めに設定
try:
    sent = sock.sendto('speed 20'.encode(encoding="utf-8"), TELLO_ADDRESS)
except:
    pass

# 問い合わせスレッド起動
askThread = threading.Thread(target=ask)
askThread.setDaemon(True)
askThread.start()


# 受信スレッド起動
recvThread = threading.Thread(target=udp_receiver)
recvThread.setDaemon(True)
recvThread.start()


battery_text = tk.StringVar()
time_text = tk.StringVar()
status_text = tk.StringVar()
battery_text.set("電池残量:")
time_text.set("飛行時間:")
status_text.set("ステータス:")


# 電池残量
battery_label = tk.Label(text='電池残量:')
battery_label.place(x=0, y=0, width = 100, height = 20)
battery_label["textvariable"] = battery_text

# 飛行時間
time_label = tk.Label(text='飛行時間:')
time_label.place(x=0, y=20, width = 100, height = 20)
time_label["textvariable"] = time_text

# 通信状況
status_label = tk.Label(text='ステータス:')
status_label.place(x=0, y=40, width = 100, height = 20)
status_label["textvariable"] = status_text

# 離陸
takeoff = tk.Button(root, text = "▲離陸", command = takeoff).place(x=0, y=60, width = 100, height = 20)

# 着陸
land = tk.Button(root, text = "▼着陸", command = land).place(x=0, y=80, width = 100, height = 20)

# 上昇(20cm)
up = tk.Button(root, text = "▲上昇", command = up).place(x=0, y=100, width = 100, height = 20)

# 下降(20cm)
down = tk.Button(root, text = "▼下降", command = down).place(x=0, y=120, width = 100, height = 20)

# 前に進む(20cm)
forward = tk.Button(root, text = "▲前に進む", command = forward).place(x=0, y=140, width = 100, height = 20)

# 後に進む(20cm)
back = tk.Button(root, text = "▼後に進む", command = back).place(x=0, y=160, width = 100, height = 20)

# 右に進む(20cm)
right = tk.Button(root, text = "▶右に進む", command = right).place(x=0, y=180, width = 100, height = 20)

# 左に進む(20cm)
left = tk.Button(root, text = "◀左に進む", command = left).place(x=0, y=200, width = 100, height = 20)

# 右回りに回転(90 deg)
cw = tk.Button(root, text = "▶右回転(90度)", command = cw).place(x=0, y=220, width = 100, height = 20)

# 左回りに回転(45 deg)
ccw = tk.Button(root, text = "◀左回転(90度)", command = ccw).place(x=0, y=240, width = 100, height = 20)

# 高速モード(速度40cm/sec)
speed40 = tk.Button(root, text = "高速モード", command = speed40).place(x=0, y=260, width = 100, height = 20)

# # 低速モード(速度20cm/sec)
speed20 = tk.Button(root, text = "低速モード", command = speed20).place(x=0, y=280, width = 100, height = 20)

# 画面をそのまま表示
root.mainloop()