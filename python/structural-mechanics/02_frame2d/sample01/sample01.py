import numpy as np
import matplotlib.pyplot as plt
import csv
import copy
import numpy as np

# リストをCSVに保存
def list_to_csv(SAVE_CSV_PATH, data):
    with open(SAVE_CSV_PATH, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data)

# 剛性マトリクス生成
def calc_stf1(el, EI, EA, ip1, ip2):
    # 2つの節点(i, j)ともに回転拘束でなければ
    if ip1==0 and ip2==0:
        #  剛性マトリクス(回転拘束状態にかかわらず共通な部分)
        stf = [[EA/el,  0, 0, -EA/el, 0, 0],
            [0,      0, 0, 0,      0, 0],
            [0,      0, 0, 0,      0, 0],
            [-EA/el, 0, 0, EA/el,  0, 0],
            [0,      0, 0, 0,      0, 0],
            [0,      0, 0, 0,      0, 0]]
    # 2つの節点(i, j)が回転拘束であれば
    elif ip1 ==1 and ip2 ==1:
        stf = [[ EA/el,          0,            0, -EA/el,            0,           0],
               [     0, 12*EI/el**3,  6*EI/el**2,      0, -12*EI/el**3,  6*EI/el**2],
               [     0,  6*EI/el**2,     4*EI/el,      0,  -6*EI/el**2,     2*EI/el],
               [-EA/el,          0,            0,  EA/el,            0,           0],
               [     0,-12*EI/el**3, -6*EI/el**2,      0,  12*EI/el**3, -6*EI/el**2],
               [     0,  6*EI/el**2,     2*EI/el,      0,  -6*EI/el**2,    4*EI/el]]
    # 2つの節点(i, j)のうち、節点iだけが回転拘束であれば
    elif ip1 ==0 and ip2 ==1:
        stf = [[ EA/el,            0,  0, -EA/el,           0,           0],
               [     0,   3*EI/el**3,  0,      0, -3*EI/el**3,  3*EI/el**2],
               [     0,            0,  0,      0,           0,           0],
               [-EA/el,            0,  0,  EA/el,           0,           0],
               [     0,  -3*EI/el**3,  0,      0,  3*EI/el**3, -3*EI/el**2],
               [     0,   3*EI/el**2,  0,      0, -3*EI/el**2,     3*EI/el]]
    # 2つの節点(i, j)のうち、節点jだけが回転拘束であれば
    elif ip1 ==1 and ip2 ==0:
        stf = [[ EA/el,           0,           0, -EA/el,           0, 0],
               [     0,  3*EI/el**3,  3*EI/el**2,      0, -3*EI/el**3, 0],
               [     0,  3*EI/el**2,     3*EI/el,      0, -3*EI/el**2, 0],
               [-EA/el,           0,           0,  EA/el,           0, 0],
               [     0, -3*EI/el**3, -3*EI/el**2,      0,  3*EI/el**3, 0],
               [     0,            0,          0,      0,           0, 0]]
    return stf

# 剛性マトリクスの座標変換
def calc_stf2(stf, cs, sn):
    z = [[cs, sn, 0,   0,   0, 0],
        [-sn, cs, 0,   0,   0, 0],
        [  0,  0, 1,   0,   0, 0],
        [  0,  0, 0,  cs,  sn, 0],
        [  0,  0, 0, -sn,  cs, 0],
        [  0,  0, 0,   0,   0, 1]] 

    # 二次元配列の生成(6*6)
    stff = [[0 for i in range(6)] for j in range(6)]
    stf2 = [[0 for i in range(6)] for j in range(6)]

    for Nj in range(0, 6):
        for NI in range(0, 6):  
            A = 0
            for i in range(0, 6):
                A = A + z[i][NI] * stf[i][Nj]
            stff[NI][Nj] = A

    for Nj in range(0, 6):
        for NI in range(0, 6):  
            A = 0
            for i in range(0, 6):
                A = A + stff[NI][i] * z[i][Nj]
            stf2[NI][Nj] = A

    return stf2, stff, z


# 剛性マトリクスの座標変換
def calc_inv(M, A):

    invA =  [[0 for i in range(120)] for j in range(120)]
    for i in range(0, M):
        for j in range(M, 2*M):
            #print("i=" + str(i) + ", j=" + str(M-1 + i))
            A[i][M + i] = 1

    # ガウスの消去法
    for k in range(0, M):
        P = A[k][k]
        for j in range(0, 2*M): 
            if P != 0:
                A[k][j] = A[k][j]/P
            else:
                A[k][j] = 0
        for i in range(0, M):
            if i == k:
                i += 1
            Q = A[i][k]
            for j in range(0, 2*M):      
                A[i][j] = A[i][j] - (Q * A[k][j])
    # 逆行列
    for i in range(0, M):
        for j in range(0, M):
            invA[i][j] = A[i][j+M]
            
    return invA


def main():
    node = 7 # 節点数
    mem = 8  # 部材数
    nlmax = 0 # 節点荷重数
    blmax = 20 # 部材荷重数
    gmax = 2   # 材料数
    icase = 4  # 荷重ケース数
    jcomb = 3  # 荷重組合せ数

    STF1_CSV_PATH = "/Users/github/sample/python/structural-mechanics/02_frame2d/sample01/stf1.csv"
    STF2_CSV_PATH = "/Users/github/sample/python/structural-mechanics/02_frame2d/sample01/stf2.csv"
    STFF_CSV_PATH = "/Users/github/sample/python/structural-mechanics/02_frame2d/sample01/stff.csv"
    Z_CSV_PATH = "/Users/github/sample/python/structural-mechanics/02_frame2d/sample01/z.csv"
    ST_CSV_PATH = "/Users/github/sample/python/structural-mechanics/02_frame2d/sample01/st.csv"
    P_CSV_PATH = "/Users/github/sample/python/structural-mechanics/02_frame2d/sample01/p.csv"
    STINV_CSV_PATH = "/Users/github/sample/python/structural-mechanics/02_frame2d/sample01/stinv.csv"

    # 材料リスト(E,A,I)
    gose = [[70000., 70000.],
            [457., 323.],
            [354397., 128832.]]

    #print(gose[2][1]) # 128832

    Lcase = ["G", "W(+)", "W(-)", "S"] 

    lcomb = [["G+W(+)", "G+W(-)", "G+S"],
            [1, 1, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]] 

    xz = [[638., 3542., 0., 638., 2090.,3542.,4181.], # X
            [0., 0., 198., 431., 959., 1488., 1720.], # Z
            [1, 1, 0, 0 , 0, 0, 0],
            [0, 0, 0, 0 , 0, 0, 0],
            [1, 1, 0, 0 , 0, 0, 0],
            [0, 0, 0, 0 , 0, 0, 0],
            [0, 0, 0, 0 , 0, 0, 0],
            [0, 0, 0, 0 , 0, 0, 0]]

    # 部材
    # 接続節点(i, j), 回転拘束(i, j), 材料番号
    buzai = [[1, 2, 1, 2, 3, 4, 5, 6],
            [4, 6, 5, 5, 4, 5, 6, 7],
            [1, 1, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [2, 2, 2, 2, 1, 1, 1, 1]]

    # 部材荷重(ケースNo、部材番号、タイプ、W/P、集中荷重点、θdeg)
    bload = [[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4],
            [5, 6, 6, 7, 8, 5, 6, 6, 7, 8, 5, 6, 6, 7, 8, 5, 6, 6, 7, 8],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [203., 406., 406., 406., 203., 2277., 4555., 4555., 4555., 2277.,2933., 5867., 5867., 5867., 2933., 2336., 4672., 4672., 4672., 2336.],
            [87., 476., 1544., 1069., 593., 87., 476., 1544., 1069., 593., 87., 476., 1544., 1069., 593., 87., 476., 1544., 1069., 593.],
            [-110, -110, -110, -110, -110, -90, -90, -90, -90, -90, 90, 90, 90, 90, 90,-110,-110,-110,-110,-110]]

    #
    grfs = [[0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0 , 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0 , 0, 0, 0]]


    # 二次元配列の生成(120*240)
    st = [[0 for i in range(120)] for j in range(240)]
    
    stf1s = []
    stf2s = []
    zs = []
    stffs = []

    ia = [0, 0]

    # 各部材ごとに剛性マトリクスを計算
    for M in range(mem):
        # 各部材の接続節点(i, j)を取得
        ia[0] = buzai[0][M]
        ia[1] = buzai[1][M]
        # 各部材の接続節点(i, j)の回転拘束状態を取得(0=非拘束、1=拘束)
        ip1 = buzai[2][M]
        ip2 = buzai[3][M]
        # 各部材の材料番号を取得
        ig = buzai[4][M]
        # 部材番号から各部材のEIとEAを算出
        EI = gose[0][ig-1] * gose[2][ig-1]
        EA = gose[0][ig-1] * gose[1][ig-1]

        # 各部材のi節点の座標を取得
        x1 = xz[0][ia[0]-1]
        z1 = xz[1][ia[0]-1]

        # 各部材のj節点の座標を取得
        x2 = xz[0][ia[1]-1]
        z2 = xz[1][ia[1]-1]

        el = ((x2-x1)**2 + (z2-z1)**2)**0.5

        stf1 = calc_stf1(el, EI, EA, ip1, ip2)

        stf1s.extend(stf1)

        cs = (x2 - x1)/el
        sn = (z2 - z1)/el

        stf2, stff, z = calc_stf2(stf1, cs, sn)
        stf2s.extend(stf2)
        stffs.extend(stff)
        zs.extend(z)
        for jj in range(0,2):
            jjj = 3 * (ia[jj] -1)
            j1 = 3 * (jj+1) - 3
            for ii in range(0, 2):
                iii = 3 * (ia[ii] -1)
                i1 = 3 * (ii+1) - 3
                for j in range(0, 3):
                    for i in range(0, 3):
                        st[i + iii][j + jjj] = st[i + iii][j + jjj] + stf2[i+i1][j+j1]

    list_to_csv(STF1_CSV_PATH, stf1s)
    list_to_csv(STF2_CSV_PATH, stf2s)
    list_to_csv(Z_CSV_PATH, zs)
    list_to_csv(STFF_CSV_PATH, stffs)
    list_to_csv(ST_CSV_PATH, st)

    ieno = 0

    # 境界条件
    for j in range(0, node):
        jj = 3 * (j+1) - 3
        for i in range(0,3):
            if xz[2*i][j] == 1:
                st[i+jj][j+jj] *= 1E+20
            elif xz[2*i][j] == 2:
                st[i+jj][j+jj] += xz[1 + 2*i][j]

            # 剛性が0ならエラー停止
            if abs(st[i+jj][i+jj]) < 0.000000001:
                ieno += 1
                print("----------")
                print(j)
                print("-node")
                print(i)
                print("-DOF")
    
    if ieno == 0:
        print("STF=0 stop")
    
    stinv = calc_inv(3*node, st)

    #stinv = np.linalg.inv(st)

    list_to_csv(STINV_CSV_PATH, stinv)
    #list_to_csv(P_CSV_PATH, P)

main()


