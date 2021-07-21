# -*- coding: utf-8
import urllib.request

# url先のHTMLファイルを開く
data = urllib.request.urlopen("https://algorithm.joho.info/" )

# HTMLの取得      
html = data.read()
html = html.decode('utf-8')
    
# 表示
print(html)
    
# HTMLファイルを閉じる
data.close()

"""
b'<!DOCTYPE html>\r\n<html lang="ja">\r\n<head>\r\n<meta charset="UTF-8"・・・・・・
"""