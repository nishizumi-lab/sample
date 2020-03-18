# -*- coding: utf-8 -*-
import socket


def main():
    # IPアドレスを取得
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)


if __name__ == "__main__":
    main()
