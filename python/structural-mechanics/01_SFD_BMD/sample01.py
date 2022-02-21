import numpy as np
import matplotlib.pyplot as plt

# グラフ画像のパス
SAVE_FIG_PATH = "/Users/github/sample/python/structural-mechanics/01_SFD_BMD/sample01.png"

# 梁が負担する分布荷重[N]
w = 100

# 梁の長さ [m]
L = 10 

# 支点反力
R = w * L/2 

# x軸の範囲
x = np.linspace(0,L,100) 

# SFD(せん断力)の計算
sfd = R - (w*x)

# MFD(曲げモーメントの計算)
mfd = (R*x) - (w*x**2/2)

# (tight_layout=Trueは軸ラベルとタイトルの重なり防止)
fig = plt.figure(figsize=(15,8), tight_layout=True)
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

# せん断力図(SFD)を描画
ax1.plot(x,sfd)
ax1.fill_between(x,sfd,color='green',hatch='||',alpha=0.47)
ax1.set_title("SFD")
ax1.set_xlabel('Length of Beam [m]')
ax1.set_ylabel('Shear Force [N]')
ax1.grid()

# 曲げモーメント図(BMD)を描画
ax2.plot(x,mfd)
ax2.fill_between(x,mfd,color='red',hatch='\\',alpha=0.5)
ax2.set_title('BMD')
ax2.set_xlabel('Length of Beam [m]')
ax2.set_ylabel('Moment [Nm]')
ax2.grid()
fig.savefig(SAVE_FIG_PATH)