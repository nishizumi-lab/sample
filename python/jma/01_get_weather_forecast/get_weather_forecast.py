# -*- coding:utf-8 -*-
import requests
from datetime import datetime

def get_latest():
    url = "https://www.jma.go.jp/bosai/amedas/data/latest_time.txt"
    with requests.get(url) as response:
        return 
    
# 気象庁から天気予報情報(JSONデータ)を取得
# ファイルパスの「270000」はエリアコード。取得したい地域に応じて適宜変更します。
JSON_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
jma_json = requests.get(JSON_URL).json()

# 今日の天気
jma_date = jma_json[0]["timeSeries"][0]["timeDefines"][0]
jma_date = datetime.fromisoformat(jma_date).strftime("%Y/%m/%d %H:%M" + "発表")
jma_area = jma_json[0]["timeSeries"][0]["areas"][0]["area"]["name"]
jma_wind = jma_json[0]["timeSeries"][0]["areas"][0]["winds"][0]
jma_wave = jma_json[0]["timeSeries"][0]["areas"][0]["waves"][0]
jma_weather = jma_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]


print("■" + jma_area + "の天気予報" + "(" + jma_date + ")")
print("天気:" + jma_weather)
print("風速:" + jma_wave)
print("風向:" + jma_wind)

"""
■大阪府の天気予報(2024/03/16 17:00発表)
天気:晴れ
風速:０．５メートル
風向:南西の風　後　北の風
"""
