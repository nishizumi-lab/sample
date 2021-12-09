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
            sent = self.sock.sendto('speed 50'.encode(encoding="utf-8"), self.tello)
        except:
            pass

        # 問い合わせスレッド起動
        askThread = threading.Thread(target=self.askTello)
        askThread.setDaemon(True)
        askThread.start()

    # ウィジェットの作成
    def create_widgets(self):
        # 離陸
        self.takeoff = tkinter.Button(self)
        self.takeoff["text"] = "離陸"  # ボタンのテキスト
        self.takeoff["command"] = self.takeoff # ボタンが押されたらtakeoffメソッドを実行
        self.takeoff.pack(side="top") # ボタンの位置

        # 着陸
        self.land = tkinter.Button(self)
        self.land["text"] = "着陸"  # ボタンのテキスト
        self.land["command"] = self.land # ボタンが押されたらlandメソッドを実行
        self.land.pack(side="bottom") # ボタンの位置


    # 通信の設定
    def initConnection(self):
        host = ''
        port = 9000
        locaddr = (host,port) 
        self.tello = ('192.168.10.1', 8889)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(locaddr)

        # 受信スレッド起動
        recvThread = threading.Thread(target=self.recvSocket)
        recvThread.setDaemon(True)
        recvThread.start()


    # 各種コマンド送信
    def takeoff(self):
        try:
            sent = self.sock.sendto('takeoff'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def land(self):
        try:
            sent = self.sock.sendto('land'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def up(self):
        try:
            sent = self.sock.sendto('up 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass
    def down(self):
        try:
            sent = self.sock.sendto('down 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def cw(self):
        try:
            sent = self.sock.sendto('cw 45'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def ccw(self):
        try:
            sent = self.sock.sendto('ccw 45'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def forward(self):
        try:
            sent = self.sock.sendto('forward 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def back(self):
        try:
            sent = self.sock.sendto('back 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def right(self):
        try:
            sent = self.sock.sendto('right 20'.encode(encoding="utf-8"), self.tello)
        except:
            pass

    def left(self):
        try:
            sent = self.sock.sendto('left 20'.encode(encoding="utf-8"), self.tello)
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
    root.geometry("300x300")
    app = Application(master=root)
    app.mainloop()