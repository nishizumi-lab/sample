# -*- coding: utf-8
import urllib.request

# url先のHTMLファイルを開く
data = urllib.request.urlopen("https://algorithm.joho.info/")

# HTMLの取得      
html = data.read()
    
# 表示
print(html)
    
# HTMLファイルを閉じる
data.close()

"""
b&#039;&lt;!DOCTYPE html&gt;\r\n&lt;html lang=&quot;ja&quot;&gt;\r\n&lt;head&gt;\r\n&lt;meta charset=&quot;UTF-8&quot;・・・・・・
"""