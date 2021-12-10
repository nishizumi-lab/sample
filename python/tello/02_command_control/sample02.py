# -*- coding: utf-8 -*-
import threading 
import socket
import time
import tkinter

class Application(tkinter.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.initConnection()
        self.create_widgets()

        # 最初にcommandコマンドを送信
        try:
            sent = self.sock.sendto('command'.encode(encoding="utf-8"), self.tello)
        except:
            pass
        # 速度を遅めに設定
        try:
            sent = self.sock.sendto('speed 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass

        # 問い合わせスレッド起動
        askThread = threading.Thread(target=self.ask)
        askThread.setDaemon(True)
        askThread.start()

    # ウィジェットの作成
    def create_widgets(self):
        # 電池残量
        self.speed_text = tkinter.Label(text='電池:')
        self.speed_text.place(x=0, y=0, width = 100, height = 20)

        # 飛行時間
        self.time_text = tkinter.Label(text='飛行時間:')
        self.time_text.place(x=0, y=20, width = 100, height = 20)

        # 通信状況
        self.status_text = tkinter.Label(text='通信状況:')
        self.status_text.place(x=0, y=40, width = 100, height = 20)

        # 離陸
        self.takeoff = tkinter.Button()
        self.takeoff["text"] = "▲離陸"  # ボタンのテキスト
        self.takeoff["command"] = self.takeoff # ボタンが押されたらtakeoffメソッドを実行
        self.takeoff.place(x=0, y=60, width = 100, height = 20) # ボタンの位置

        # 着陸
        self.land = tkinter.Button()
        self.land["text"] = "▼着陸" 
        self.land["command"] = self.land
        self.land.place(x=0, y=80, width = 100, height = 20)

        # 上昇(20cm)
        self.up = tkinter.Button()
        self.up["text"] = "▲上昇"
        self.up["command"] = self.up 
        self.up.place(x=0, y=100, width = 100, height = 20)

        # 下降(20cm)
        self.down = tkinter.Button()
        self.down["text"] = "▼下降" 
        self.down["command"] = self.down 
        self.down.place(x=0, y=120, width = 100, height = 20)

        # 前に進む(20cm)
        self.forward = tkinter.Button()
        self.forward["text"] = "▲前に進む" 
        self.forward["command"] = self.forward 
        self.forward.place(x=0, y=140, width = 100, height = 20)

        # 後に進む(20cm)
        self.back = tkinter.Button()
        self.back["text"] = "▼後に進む" 
        self.back["command"] = self.back 
        self.back.place(x=0, y=160, width = 100, height = 20)

        # 右に進む(20cm)
        self.right = tkinter.Button()
        self.right["text"] = "▶右に進む" 
        self.right["command"] = self.right 
        self.right.place(x=0, y=180, width = 100, height = 20)

        # 左に進む(20cm)
        self.left = tkinter.Button()
        self.left["text"] = "◀左に進む"
        self.left["command"] = self.left
        self.left.place(x=0, y=200, width = 100, height = 20)

        # 右回りに回転(90 deg)
        self.cw = tkinter.Button()
        self.cw["text"] = "▶右回転(90度)" 
        self.cw["command"] = self.cw 
        self.cw.place(x=0, y=220, width = 100, height = 20)

        # 左回りに回転(45 deg)
        self.ccw = tkinter.Button()
        self.ccw["text"] = "◀左回転(90度)"
        self.ccw["command"] = self.ccw 
        self.ccw.place(x=0, y=240, width = 100, height = 20)

        # 高速モード(速度40cm/sec)
        self.speed40 = tkinter.Button()
        self.speed40["text"] = "高速モード" 
        self.speed40["command"] = self.speed40 
        self.speed40.place(x=0, y=260, width = 100, height = 20)

        # 低速モード(速度20cm/sec)
        self.speed20 = tkinter.Button()
        self.speed20["text"] = "低速モード" 
        self.speed20["command"] = self.speed20 
        self.speed20.place(x=0, y=280, width = 100, height = 20)

    # 通信の設定
    def initConnection(self):
        host = ''
        port = 9000
        locaddr = (host,port) 
        self.tello = ('192.168.10.1', 8889)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(locaddr)

        # 受信スレッド起動
        recvThread = threading.Thread(target=self.recv)
        recvThread.setDaemon(True)
        recvThread.start()


    # 離陸
    def takeoff(self):
        try:
            sent = self.sock.sendto('takeoff'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 着陸
    def land(self):
        try:
            sent = self.sock.sendto('land'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 上昇(20cm)
    def up(self):
        try:
            sent = self.sock.sendto('up 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 下降(20cm)
    def down(self):
        try:
            sent = self.sock.sendto('down 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 前に進む(20cm)
    def forward(self):
        try:
            sent = self.sock.sendto('forward 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 後に進む(20cm)
    def back(self):
        try:
            sent = self.sock.sendto('back 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 右に進む(20cm)
    def right(self):
        try:
            sent = self.sock.sendto('right 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 左に進む(20cm)
    def left(self):
        try:
            sent = self.sock.sendto('left 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 右回りに回転(90 deg)
    def cw(self):
        try:
            sent = self.sock.sendto('cw 90'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 左回りに回転(90 deg)
    def ccw(self):
        try:
            sent = self.sock.sendto('ccw 90'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 高速モード(速度40cm/sec)
    def speed40(self):
        try:
            sent = self.sock.sendto('speed 40'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # 低速モード(速度20cm/sec)
    def speed20(self):
        try:
            sent = self.sock.sendto('speed 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    # Telloからのレスポンス受信
    def recv(self):
        while True: 
            try:
                data, server = self.sock.recvfrom(1518)
                resp = data.decode(encoding="utf-8").strip()
                if resp.isdecimal():    # 数字だけなら充電量
                    self.batteryLabel.setText(resp + "%")
                elif resp[-1:] == "s":  # 最後の文字がsなら飛行時間
                    self.timeLabel.setText(resp)
                elif resp == "OK":      # OKは黒
                    self.label.setStyleSheet("color:black;")
                    self.label.setText(resp)
                else:                   # それ以外は赤
                    self.label.setStyleSheet("color:red;")
                    self.label.setText(resp)
            except:
                pass

    # 問い合わせ
    def ask(self):
        while True:
            try:
                sent = self.sock.sendto('battery?'.encode(encoding="utf-8"), self.tello)
            except:
                pass
            time.sleep(0.5)

            try:
                sent = self.sock.sendto('time?'.encode(encoding="utf-8"), self.tello)
            except:
                pass
            time.sleep(0.5)

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry("200x600")
    app = Application(master=root)
    app.mainloop()