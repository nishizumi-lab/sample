import requests

LINE_NOTIFY_TOKEN= '取得したLINEのトークン'
message = '自動通知するメッセージ'

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ LINE_NOTIFY_TOKEN}
payload = {"message" :  message}

r = requests.post(url ,headers = headers ,params=payload)

print(r)