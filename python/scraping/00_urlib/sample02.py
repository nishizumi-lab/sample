# -*- coding: utf-8
import urllib.request

# url先のHTMLファイルを開く
data = urllib.request.urlopen("https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample01/index.html")

# HTMLの取得      
html = data.read()
html = html.decode('utf-8')
    
# 表示
print(html)
    
# HTMLファイルを閉じる
data.close()

"""
<!doctype html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>ページタイトル</title>
</head>
<body>
  <div class="header">ヘッダーです</div>
  <div class="main">
    <h1>H1の見出しです</h1>
    <p>文章1です</p>
  </div>
  <div class="footer">
    <p>フッターです</p>
    <a href="#">リンク1</a>
        <a href="#">リンク2</a>
  </div>
</body>
</html>
"""