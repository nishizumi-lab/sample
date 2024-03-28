import requests

LINE_NOTIFY_TOKEN= '取得したLINEのトークン'
message = 'ご安全に！'
filepath = '/Users/github/sample/python/line/01_LINE_Notify/mujiko.png'

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ LINE_NOTIFY_TOKEN}
payload = {"message" :  message}
files = {'imageFile': open(filepath, "rb")}

r = requests.post(url ,headers = headers ,params=payload, files=files)

print(r)