# -*- coding: utf-8 -*-
import sys
sys.path.append('/Users/github/sample/python/basic/mymodule/sample02/my')
import my


def main():
    # インスタンスの生成
    my_class = my.MyClass()
    # メソッドの呼び出し
    my_class.my_method("にゃんぱすー")

if __name__ == "__main__":
    main()

"""
初期化
Test にゃんぱすー
"""