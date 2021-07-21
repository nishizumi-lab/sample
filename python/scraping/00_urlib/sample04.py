#-*- using:utf-8 -*-
import urllib.request

def check_url(url):
    flag = True
    try:
        f = urllib.request.urlopen(url)
        print('OK:', url)
        f.close()
    except urllib.request.HTTPError:
        print('Not found:', url)
        flag = False

    return flag


url = "https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/scraping/00_sample_data/sample01/index.html"

print(check_url(url)) # True