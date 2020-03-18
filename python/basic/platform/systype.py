# -*- coding: utf-8 -*-
import platform

def main():
    # システムの種類を取得
    systype = platform.system()
    # 取得した情報を表示
    print(systype)

if __name__ == '__main__':
    main()
