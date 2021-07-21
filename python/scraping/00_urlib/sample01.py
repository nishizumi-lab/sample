# -*- coding: utf-8
import urllib.request

# url先のHTMLファイルを開く
data = urllib.request.urlopen("https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample01/index.html")

# HTMLの取得      
html = data.read()
    
# 表示
print(html)
    
# HTMLファイルを閉じる
data.close()

"""
b'<!doctype html>\r\n<html lang="ja">\r\n<head>\r\n  <meta charset="UTF-8">\r\n  
<title>\xe3\x83\x9a\xe3\x83\xbc\xe3\x82\xb8\xe3\x82\xbf\xe3\x82\xa4\xe3\x83\x88\xe3\x83\xab</title>
\r\n</head>\r\n<body>\r\n  <div class="header">\xe3\x83\x98\xe3\x83\x83\xe3\x83\x80\xe3\x83\xbc\xe3\x81\xa7\xe3\x81\x99</div>\r\n  <div class="main">\r\n    <h1>H1\xe3\x81\xae\xe8\xa6\x8b\xe5\x87\xba\xe3\x81\x97\xe3\x81\xa7\xe3\x81\x99</h1>\r\n    <p>\xe6\x96\x87\xe7\xab\xa01\xe3\x81\xa7\xe3\x81\x99</p>\r\n  </div>\r\n  <div class="footer">\r\n    <p>\xe3\x83\x95\xe3\x83\x83\xe3\x82\xbf\xe3\x83\xbc\xe3\x81\xa7\xe3\x81\x99</p>\r\n    <a href="#">\xe3\x83\xaa\xe3\x83\xb3\xe3\x82\xaf1</a>\r\n\t<a href="#">\xe3\x83\xaa\xe3\x83\xb3\xe3\x82\xaf2</a>\r\n  </div>\r\n</body>\r\n</html>'
"""