#coding:UTF-8
import requests
import subprocess
import time
import sys
import datetime

token = '取得したLINEのトークン'

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ token}
payload = {"message" :  globalIP}
r = requests.post(url ,headers = headers ,params=payload)

print(r)