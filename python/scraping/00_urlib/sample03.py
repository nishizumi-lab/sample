# -*- coding: utf-8
import urllib.request
    
# 取得先URL
url = "https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample01/index.html" 

# ユーザーエージェント情報を設定
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]

# HTMLファイルを開く
data = opener.open(url)
    
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