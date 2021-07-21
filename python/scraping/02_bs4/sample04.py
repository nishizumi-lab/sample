# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.error
import urllib.request
import os
import time


# ダウンロード(画像URL, 保存先パス)
def download_img(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)


# ダウンロードした画像ファイルの保存先パス
dst_dir = '/Users/github/sample/python/scraping/02_bs4/sample04'

# urlのHTMLを取得
url = 'https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample03/index.html'

# User-Agent
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'


# リクエスト
req = urllib.request.Request(url, headers={'User-Agent': ua})

# HTML取得
html = urllib.request.urlopen(req)

# HTMLパース
soup = BeautifulSoup(html, "html.parser")

# imgタグを取得
img_tags = soup.find_all('img')

# imgタグのURL格納用
img_urls = []

# imgタグのURLを抽出
for img in img_tags:
    img_urls.append(img.get('src'))


# ダウンロード間隔時間（サーバー負荷対策のため1sec以上は空ける）
sleep_time = 1

for img_url in img_urls:
    filename = os.path.basename(img_url)
    # 保存先パス=保存先ディレクトリ+ファイル名
    dst_path = os.path.join(dst_dir, filename)
    time.sleep(sleep_time)
    print('DL:', img_url)
    download_img(url, dst_path)

"""
DL: ./images/1.jpg
DL: ./images/2.jpg
DL: ./images/3.jpg
"""