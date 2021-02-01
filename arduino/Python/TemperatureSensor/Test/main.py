# -*- coding: utf-8 -*-
import serial
import datetime

def main():
    
    i = 0
    ser = serial.Serial("COM5")  # Arduinoが接続されているコムポートを指定
    while(i != 10):
        todaydetail = datetime.datetime.today()
        line = ser.readline()   # 行終端まで読み込む
        line = line.rstrip()    # 行終端コード削除
        print(todaydetail.strftime("%Y/%m/%d %H:%M:%S") + " > " + line + "[C]")
        i+=1

    ser.close()
    print("End")

if __name__ == '__main__':
    main()
