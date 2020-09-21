# -*- coding: utf-8 -*-
import csv

# 読み込み
def read_csv(filename):
    f = open(filename, "r")
    csv_data = csv.reader(f)
    list = [ e for e in csv_data]
    f.close()
    return list

# リストの更新
def update_list2d(list, data):
    for i in range(len(list)):
        if list[i][0]==data[0]: list[i] = data
    return list

# 書き込み
def write_csv(filename, list):
   with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(list)   

   f.close()

def main():
    # CSVファイルのパス
    csv_path = "C:/github/sample/python/csv/02_update/data.csv"

    # CSVファイルのロード
    csv_data = read_csv(csv_path)

    # リストを更新
    data = ["2017-01-01 01:00", 20, 50, 1030, 5]
    csv_data2 = update_list2d(csv_data, data)

    # 更新後のリストを書き込み
    write_csv(csv_path, csv_data2)
    
if __name__=='__main__':
    main()

"""
更新前：2017-01-01 01:00, 0, 0, 0, 0
↓
更新後：2017-01-01 01:00, 20, 50, 1030, 5
"""