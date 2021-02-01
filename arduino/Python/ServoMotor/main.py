# -*- coding: utf-8 -*-
import serial

def main():

    # シリアル通信の設定(
    ser = serial.Serial("COM7", 9600, timeout=1)
    while True:
        # 入力待機（回転させたい角度を入力）
        deg = raw_input()
        # eが入力されたら終了
        if(deg == "e"):
            ser.close()
            break;
        # 回転角と終端文字を送信
        ser.write(str(deg)+"\0")


if __name__ == '__main__':
    main()
