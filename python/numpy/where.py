# -*- coding: utf-8 -*-
import numpy as np

def main():

    y = np.array([8,9,10,11,15,18,22,21,20,29])    # データ(気温)
    x = np.where((y>=10)&(y<20))
    # 結果を表示
    print(u"10以上20未満のデータがある要素番号："+str(x[0]))



if __name__ == '__main__':
    main()
