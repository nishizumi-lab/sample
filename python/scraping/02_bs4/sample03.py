# -*- coding: utf-8 -*-
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

def table_to_csv(file_path, url, selecter):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    # セレクタ(タグ：table、クラス：test)
    table = soup.findAll("table", selecter)[0]

    trs = table.findAll("tr")
    # ファイルオープン
    csv_file = open(file_path, 'wt', newline = '', encoding = 'utf-8')
    csv_write = csv.writer(csv_file)

    for tr in trs:
        csv_data = []
        # 1行ごとにtd, tr要素のデータを取得してCSVに書き込み
        for cell in tr.findAll(['td', 'th']):
            csv_data.append(cell.get_text())
        csv_write.writerow(csv_data)

    # ファイルクローズド
    csv_file.close()

# URLの指定
url = 'https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample02/index.html'

# セレクタ
selecter = {"class":"test"}

# 指定したURL・セレクタの表のデータをCSVに保存
table_to_csv("/Users/github/sample/python/scraping/02_bs4/sample03.csv", url, selecter)
