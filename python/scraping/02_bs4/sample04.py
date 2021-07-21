#-*- using:utf-8 -*-
import urllib

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


url = "https://algorithm.joho.info"

print(check_url(url)) # True