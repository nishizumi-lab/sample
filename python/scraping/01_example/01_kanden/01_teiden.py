import csv

import requests
from bs4 import BeautifulSoup

url = 'https://algorithm.joho.info/programming/python/beautifulsoup-table-to-csv/'

# セルコピー True:空白、False:コピー
flag = False

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

r = requests.get(url, headers=headers)

if r.status_code == requests.codes.ok:

    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('table', class_='service_area sub')

    trs = [i for i in table.find_all('tr')]

    # 最大行数
    tr_max = len(trs)

    # 空リスト作成
    data = [[] for _ in range(tr_max)]

    for j, tr in enumerate(trs):
        for td in tr.find_all(['th', 'td']):

            cell = td.get_text(strip=True)

            rowspan = td.get('rowspan')
            colspan = td.get('colspan')

            row = int(rowspan) if rowspan else 1
            col = int(colspan) if colspan else 1

            for y in range(row):

                for x in range(col):

                    data[j + y].append(cell)

                    if cell and flag:
                        cell = ''

    with open('/Users/github/sample/python/scraping/01_example/01_kanden/ebo.csv', 'w') as fw:
        writer = csv.writer(fw, dialect='excel', lineterminator='\n')
        writer.writerows(data)
