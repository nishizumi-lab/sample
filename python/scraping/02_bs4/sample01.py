# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

# urlのHTMLを取得
url = 'https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample01/index.html'
html = urllib.request.urlopen(url)

# htmlをBeautifulSoupでパース
soup = BeautifulSoup(html, "html.parser")

# タイトル要素の取得
print(soup.title) # <title>ページタイトル</title>

# タイトル要素の文字列を取得
print(soup.title.string) # ページタイトル