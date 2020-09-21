# -*- coding: utf-8 -*-
import csv
import datetime as dt

# 365日*24時間分の日付を取得
def get_dates():
    date = dt.datetime(2017, 1, 1, 0, 0)
    dates = []
    for i in range(365*24):
        dates.append(date.strftime('%Y-%m-%d %H:%M'))
        date += dt.timedelta(hours=1)
    return dates

# 2次元リストをCSVファイルに保存
def write_csv(csv_path, data):
   with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)   

    
def main():
    # CSVファイルのパス
    csv_path = "C:/github/sample/python/csv/03_make_date_list/data.csv"

    # 365日*24時間分の日付を取得してリストを作成
    dates = get_dates()
    data = [dates] # 2次元リストに変換
    data = list(map(list, zip(*data))) # リストの転置

    # CSVにリストを書き込み
    write_csv(csv_path, data)
    
if __name__=='__main__':
    main()

"""
data.csvの中身

2017/1/1 0:00
2017/1/1 1:00
2017/1/1 2:00
2017/1/1 3:00
2017/1/1 4:00
︙
2017/12/31 21:00
2017/12/31 22:00
2017/12/31 23:00
"""
