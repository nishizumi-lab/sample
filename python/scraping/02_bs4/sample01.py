# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

# urlのHTMLを取得
url = 'https://algorithm.joho.info/'
html = urllib.request.urlopen(url)

# htmlをBeautifulSoupでパース
soup = BeautifulSoup(html, "html.parser")

# タイトル要素の取得
print(soup.title) # <title>アルゴリズム雑記</title>

# タイトル要素の文字列を取得
print(soup.title.string) # アルゴリズム雑記