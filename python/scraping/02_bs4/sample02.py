# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup

# urlのHTMLを取得
url = 'https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample01/index.html'
html = urllib.request.urlopen(url)

# HTMLパース
soup = BeautifulSoup(html, 'html.parser')

# 先頭のdivタグを取得
div = soup.find('div')
print('div=', div)

"""
div= <div class="header">ヘッダーです</div>
"""

# すべてのdivタグを取得
div_all = soup.find_all('div')
print('div_all=', div_all)

"""
div_all= [
<div class="header">ヘッダーです</div>, 
<div class="main">
<h1>H1の見出しです</h1>
<p>文章1です</p>
</div>, 
<div class="footer">
<p>フッターです</p>
<a href="#">リンク1</a>
<a href="#">リンク2</a>
</div>
]
"""