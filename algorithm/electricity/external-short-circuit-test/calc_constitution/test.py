#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd

# https://colab.research.google.com/drive/1e82yrx4YhI1rPnl0gTdaZXmYYxHTfYyf

# 試験条件
I_target = 200 # 目標電流値[A]
V_target = 50 # 目標電圧値[V]
test_r = 0 # 試験体の抵抗[mΩ]
other_r = 0 # その他の抵抗値（端子台など）

# 保存先パス
# 例：C:/prog/python/test
path = "C:/prog/python/test"

# 配線抵抗[mΩ]
LINE_R = 5 

# 電源のパラメータ
R = 5 # 電源1つ(1直1並)あたりの内部抵抗[mΩ]
SERIES_N = 4 # 電源の最大直列数
PARALLEL_N = 4 # 電源の最大並列数
POWER_V_MIN = 20.0 # 電源1つ(1直1並)あたりの最小電圧[V]
POWER_V_MAX = 30.0 # 電源1つ(1直1並)あたりの最大電圧[V]

# 外部短絡装置の可変抵抗組み合わせパターン(昇順に並べる)
LIST_EXT_R = [100, 200, 300, 400, 500]

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
               Imin    Imax  Vmin  Vmax  I[A](50V)  V[V](200A)  I_error  V_error
Pattern
2s1p-ext200  186.05  279.07  60.0  40.0     232.56       43.00     7.00    32.56
2s2p-ext200  190.48  285.71  60.0  40.0     238.09       42.00     8.00    38.09
2s3p-ext200  192.00  288.00  60.0  40.0     240.00       41.67     8.33    40.00
2s4p-ext200  192.77  289.16  60.0  40.0     240.97       41.50     8.50    40.97

----------------------------------------
【試験電流条件に最も近い構成】
構成： 2s1p-ext200
Imin          186.05
Imax          279.07
Vmin           60.00
Vmax           40.00
I[A](50V)     232.56
V[V](200A)     43.00
I_error         7.00
V_error        32.56
Name: 2s1p-ext200, dtype: float64

----------------------------------------
【試験電圧条件に最も近い構成】
構成： 2s1p-ext200
Imin          186.05
Imax          279.07
Vmin           60.00
Vmax           40.00
I[A](50V)     232.56
V[V](200A)     43.00
I_error         7.00
V_error        32.56
Name: 2s1p-ext200, dtype: float64
"""
