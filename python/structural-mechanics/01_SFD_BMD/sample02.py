import numpy as np
import matplotlib.pyplot as plt

# グラフ画像のパス
SAVE_FIG_PATH = "/Users/github/sample/python/structural-mechanics/01_SFD_BMD/sample02.png"

# サンプル数
N = 100

# 梁が負担する集中荷重[N]
P = 100

# 梁の長さ [m]
L = 10 

# 支点Aから集中荷重の作用点までの長さ
L1 = 5

# 支点Aの反力
RA = ((L-L1)/L)*P

# x軸の範囲
x1 = np.linspace(0,L1,N) 
x2 = np.linspace(L1,L,N) 
x = np.r_[x1, x2]

# SFD(せん断力)の計算
sfd1 = np.full(N, RA)
sfd2 = np.full(N, -RA)
sfd = np.r_[sfd1, sfd2]

# BMD(曲げモーメントの計算)
bmd1 = RA * x1
bmd2 = RA * x2 - P*(x2-L1)
bmd = np.r_[bmd1, bmd2]

# (tight_layout=Trueは軸ラベルとタイトルの重なり防止)
fig = plt.figure(figsize=(10,8), tight_layout=True)
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
ax2.plot(x,bmd)
ax2.fill_between(x, bmd,color='red',hatch='\\',alpha=0.5)
ax2.set_title('BMD')
ax2.set_xlabel('Length of Beam [m]')
ax2.set_ylabel('Moment [Nm]')
ax2.grid()
fig.savefig(SAVE_FIG_PATH)