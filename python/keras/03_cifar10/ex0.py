# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import cifar10


def main():
    # CIFAR-10のデータセットを取得
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()

    # 3x3枚の画像を表示
    plt.figure(figsize=(3, 3))

    for i in range(9):
        # 0-49999の整数値をランダムに取得
        index = np.random.randint(0, 50000)
        plt.subplot(3, 3, i+1)
        plt.imshow(x_train[index])
        # x-y軸の目盛りを消去
        plt.tick_params(labelbottom='off')
        plt.tick_params(labelleft='off')

    plt.show()


if __name__ == '__main__':
    main()
