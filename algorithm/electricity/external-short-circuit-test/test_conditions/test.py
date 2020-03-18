#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd

# 試験条件
I_target = 5000 # 目標電流値[A]
V_target = 600 # 目標電圧値[V]
test_r = 0 # 試験体の抵抗[mΩ]
other_r = 0 # その他の抵抗値（端子台など）

# 保存先パス
path = "C:/prog/python/test"

# 配線抵抗[mΩ]
LINE_R = 7 

# 電源のパラメータ
R = 22 # 電源1つ(1直1並)あたりの内部抵抗[mΩ]
SERIES_N = 8 # 電源の最大直列数
PARALLEL_N = 8 # 電源の最大並列数
POWER_V_MIN = 70.4 # 電源1つ(1直1並)あたりの最小電圧[V]
POWER_V_MAX = 121.6 # 電源1つ(1直1並)あたりの最大電圧[V]

# 外部短絡装置の可変抵抗組み合わせパターン(昇順に並べる)
LIST_EXT_R = [1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23, 29, 30, 31, 32, 33, 34, 35, 36, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 67, 68, 69, 70, 71, 72, 73, 79, 80, 81, 82, 83, 84, 85, 86, 95, 96, 97, 98, 99, 100, 101, 102]

# 合成抵抗の計算
def calc_rx(r, series_num, parallel_num):
    # 直列分の計算
    series_r = np.repeat(r*series_num, parallel_num)
    # 並列分の計算
    return 1. /np.sum(1. /series_r)

# インピーダンスの一覧表を作成
def make_table(r, series_num, parallel_num, test_r, ext_list_r, line_r, v_max, v_min):
    # 電源の内部抵抗を計算（直並列のパターンごと）
    table_r = {}
    for j in range(series_num):
        list_r = []
        for i in range(parallel_num):
           if((j+1) * (i+1) < 9):
               table_r[str(j+1)+"s" + str(i+1) + "p"] = calc_rx(r, j+1, i+1)

    df = pd.DataFrame(pd.Series(data=table_r, name="power_imp"))
    df.index.name = "sp_pattern"

    # 直並列数のパターンを列に追加
    list_series_num = []
    list_parallel_num = []

    for j in range(0, series_num):
        for i in range(0, parallel_num):
           if((j+1) * (i+1) < 9):
               list_series_num.append(j + 1)
               list_parallel_num.append(i + 1)

    df["series_num"] = list_series_num
    df["parallel_num"] = list_parallel_num

    # 電源電圧の最大値、最小値を直並列のパターンごとに計算し、列に追加
    df["Vmax"] = df["series_num"] * v_max
    df["Vmin"] = df["series_num"] * v_min


    # 回路網の全抵抗（電源の内部抵抗 + 外部短絡装置の抵抗 + 配線抵抗）を計算し、列に追加
    for ext_r in ext_list_r:
        df["All_Imp_ext" + str(ext_r)] = df["power_imp"] + ext_r + line_r + test_r

    # 電流の最大値を計算（電源の組合せパターン毎）
    for ext_r in ext_list_r:
        df["Imax_ext" + str(ext_r)] = df["Vmax"]/df["All_Imp_ext" + str(ext_r)] * 1000

    # 電流の最小値を計算（電源の組合せパターン毎）
    for ext_r in ext_list_r:       
        df["Imin_ext" + str(ext_r)] = df["Vmin"]/df["All_Imp_ext" + str(ext_r)] * 1000
    return df

def search_pattern(df, ext_list_r, I_target, V_target):
    # 目標電流を満たす電源・外部短絡抵抗の組合せを検索（結果をマスクで出力）
    df_imin = df.loc[:, 'Imin_ext' + str(ext_list_r[0]):'Imin_ext' + str(ext_list_r[-1])]
    df_imax = df.loc[:, 'Imax_ext' + str(ext_list_r[0]):'Imax_ext' + str(ext_list_r[-1])]
    df_imin_mask = (df_imin <= I_target)
    df_imax_mask = (I_target <= df_imax)

    # 目標電圧を満たす電源・外部短絡抵抗の組合せを検索（結果をマスクで出力）
    df_vmin = df.loc[:, 'Vmin']
    df_vmax = df.loc[:, 'Vmax']
    df_vmin_mask = (df_vmin <= V_target)
    df_vmax_mask = (V_target <= df_vmax)

    df_target = df_imin.copy()

    # 目標電圧・目標電流を両方満たす電源・外部短絡抵抗の組合せを検索（結果をマスクで出力）
    for ext_r in ext_list_r:       
        df_target['ext' + str(ext_r)] = df_imin_mask['Imin_ext' + str(ext_r)] & df_imax_mask['Imax_ext' + str(ext_r)] & df_vmin_mask  & df_vmax_mask
    
    df_target = df_target.loc[:, "ext" + str(ext_list_r[0]):"ext" + str(ext_list_r[-1])]
    sp_pattern_list = df_target.index.tolist()
    df_target = df_target.transpose()
    
    result_ext_dict = {}

    # 目標電圧・目標電流を電源・両方満たす外部短絡抵抗の組合せを取得
    for sp_pattern in sp_pattern_list:
        result = df_target[df_target[sp_pattern] == True].index.tolist()
        if result:
            result_ext_dict[sp_pattern] = df_target[df_target[sp_pattern] == True].index.tolist()

    return result_ext_dict

def save_result(path, df, result_dict, I_target, V_target):
    df_result = pd.DataFrame(columns=['Imin', 'Imax', 'Vmin', 'Vmax', 'I[A](' + str(V_target) +'V)', 'V[V](' + str(I_target) +'A)', 'I_error', 'V_error' ] )
    for key, value in result_dict.items():
        for i in range(len(value)):
            # 試験条件を満たす電流、電圧の最小値、最大値
            I_min = round(df.loc[key, "Imin_" + value[i]],2)
            I_max = round(df.loc[key, "Imax_" + value[i]],2)
            V_max = round(df.loc[key, "Vmax"], 2)
            V_min = round(df.loc[key, "Vmin"], 2)
            dI = (I_max - I_min) * ((V_max - V_target) / (V_max - V_min))
            I = round(I_max - dI, 2)
            dV = (V_max - V_min) * ((I_max - I_target) / (I_max - I_min))
            V = round(V_max - dV, 2)  
            df_result.loc[key + "-" + str(value[i])] = [I_min, I_max, V_max, V_min, I, V, abs(V-V_target), abs(I-I_target)]      


    # インデックス名を「Pattern」に設定
    df_result.index.name ='Pattern'
    
    # データフレームが空の場合（試験条件を満たす構成が無い）
    if df_result.empty:
        print("試験条件を満たす構成は存在しません。") 
        return -1

    # データフレームが空でない場合（試験条件を満たす構成がある）   
    print('----------------------------------------')
    print('【試験条件を満たす構成】')
    print(df_result)

    print('\n----------------------------------------')
    print('【試験電流条件に最も近い構成】')
    print('構成：', df_result['I_error'].idxmin())
    ss_ierror_min = df_result.loc[df_result['I_error'].idxmin()]
    print(ss_ierror_min)
    print('\n----------------------------------------')
    print('【試験電圧条件に最も近い構成】')
    print('構成：', df_result['V_error'].idxmin())
    ss_verror_min = df_result.loc[df_result['V_error'].idxmin()]
    print(ss_verror_min)

    # 結果をCSVファイルに出力
    df_result.to_csv(path + '/result.csv')
    ss_ierror_min.to_csv(path + '/result_ierror_min.csv', header=False)
    ss_verror_min.to_csv(path + '/result_verror_min.csv', header=False)
    df.to_csv(path + '/table.csv')

    return df_result



def main():
    # 一覧表を作成・保存
    df = make_table(R, SERIES_N, PARALLEL_N, test_r + other_r, LIST_EXT_R, LINE_R, POWER_V_MAX, POWER_V_MIN)

    # 試験条件を満たす電源・外部短絡抵抗の組合せを取得
    result_dict = search_pattern(df, LIST_EXT_R, I_target, V_target)
    
    # 結果の保存 
    df_result = save_result(path, df, result_dict, I_target, V_target)

if __name__ == "__main__":
    main()

"""
----------------------------------------
【試験条件を満たす構成】
              Imin     Imax   Vmin   Vmax  I[A](600V)  V[V](5000A)  I_error  V_error
Pattern
5s1p-ext1  2983.05  5152.54  608.0  352.0     5084.74        590.0     10.0    84.74
5s1p-ext2  2957.98  5109.24  608.0  352.0     5042.01        595.0      5.0    42.01
5s1p-ext3  2933.33  5066.67  608.0  352.0     5000.00        600.0      0.0     0.00
5s1p-ext4  2909.09  5024.79  608.0  352.0     4958.67        605.0      5.0    41.33
6s1p-ext1  3017.14  5211.43  729.6  422.4     4285.71        700.0    100.0   714.29
6s1p-ext2  2995.74  5174.47  729.6  422.4     4255.32        705.0    105.0   744.68
6s1p-ext3  2974.65  5138.03  729.6  422.4     4225.35        710.0    110.0   774.65
6s1p-ext4  2953.85  5102.10  729.6  422.4     4195.81        715.0    115.0   804.19
6s1p-ext5  2933.33  5066.67  729.6  422.4     4166.67        720.0    120.0   833.33
6s1p-ext6  2913.10  5031.72  729.6  422.4     4137.93        725.0    125.0   862.07
7s1p-ext1  3041.98  5254.32  851.2  492.8     3703.71        810.0    210.0  1296.29
7s1p-ext2  3023.31  5222.09  851.2  492.8     3680.98        815.0    215.0  1319.02
7s1p-ext3  3004.88  5190.24  851.2  492.8     3658.54        820.0    220.0  1341.46
7s1p-ext4  2986.67  5158.79  851.2  492.8     3636.37        825.0    225.0  1363.63
7s1p-ext5  2968.67  5127.71  851.2  492.8     3614.45        830.0    230.0  1385.55
7s1p-ext6  2950.90  5097.01  851.2  492.8     3592.82        835.0    235.0  1407.18
7s1p-ext7  2933.33  5066.67  851.2  492.8     3571.43        840.0    240.0  1428.57
8s1p-ext1  3060.87  5286.96  972.8  563.2     3260.87        920.0    320.0  1739.13
8s1p-ext2  3044.32  5258.38  972.8  563.2     3243.24        925.0    325.0  1756.76
8s1p-ext3  3027.96  5230.11  972.8  563.2     3225.81        930.0    330.0  1774.19
8s1p-ext4  3011.76  5202.14  972.8  563.2     3208.55        935.0    335.0  1791.45
8s1p-ext5  2995.74  5174.47  972.8  563.2     3191.49        940.0    340.0  1808.51
8s1p-ext6  2979.89  5147.09  972.8  563.2     3174.60        945.0    345.0  1825.40
8s1p-ext7  2964.21  5120.00  972.8  563.2     3157.89        950.0    350.0  1842.11

----------------------------------------
【試験電流条件に最も近い構成】
構成： 5s1p-ext3
Imin           2933.33
Imax           5066.67
Vmin            608.00
Vmax            352.00
I[A](600V)     5000.00
V[V](5000A)     600.00
I_error           0.00
V_error           0.00
Name: 5s1p-ext3, dtype: float64

----------------------------------------
【試験電圧条件に最も近い構成】
構成： 5s1p-ext3
Imin           2933.33
Imax           5066.67
Vmin            608.00
Vmax            352.00
I[A](600V)     5000.00
V[V](5000A)     600.00
I_error           0.00
V_error           0.00
Name: 5s1p-ext3, dtype: float64
"""
