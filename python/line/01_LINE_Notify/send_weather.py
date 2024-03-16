# -*- coding: utf-8 -*-
import requests
from datetime import datetime

# 天気概況を取得
def get_overview_forecast(AREA_NUM):
    json_url = f"https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{AREA_NUM}.json"
    req = requests.get(json_url)
    data = req.json()
    return "\n".join(data["text"].split())

# 天気予報を取得
def get_weather_forecast(AREA_NUM, DETAIL_AREA_NUM):
    json_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{AREA_NUM}.json"
    req = requests.get(json_url)
    data = req.json()
    data = data[0]["timeSeries"][0]["areas"] 
    # インデックスを取得
    data_index = [num for num, i in enumerate(data) if i["area"]["code"] == DETAIL_AREA_NUM][0]

    weather_info = data[data_index]["weathers"]
    return  " ".join(weather_info[1].split())

# アメダスの情報を取得
def get_amedas_data(OBSERV_POINT_NUM, time_yyyymmdd, time_h3):
    # アメダス
    json_url = f"https://www.jma.go.jp/bosai/amedas/data/point/{OBSERV_POINT_NUM}/{time_yyyymmdd}_{time_h3}.json"
    
    print(json_url)
    req = requests.get(json_url)
    data = req.json()
    
    # 最新のアメダスデータが入っているkey
    latest_key = max(data) 

    # 気温を取得
    temp = str(data[latest_key]["temp"][0])

    # 湿度を取得
    humidity = str(data[latest_key]["humidity"][0])

    # 10分毎の降水量を取得
    prec10m = str(data[latest_key]["precipitation10m"][0])

    # 大気圧を取得
    pressure = str(data[latest_key]["pressure"][0])

    now_datas = {"temp":temp, "humidity":humidity, "prec10m":prec10m, "pressure":pressure}
    return now_datas

def get_weather_datas():
    # エリア番号(大阪は270000)
    AREA_NUM = "270000" 

    # 詳細予報のエリア番号(大阪府は270000)
    DETAIL_AREA_NUM = "270000" 

    # 観測所番号(大阪市中央区大手前　大阪管区気象台は62078)
    OBSERV_POINT_NUM = "62078" 

    # 最新時刻を取得
    latest_time_req = requests.get("https://www.jma.go.jp/bosai/amedas/data/latest_time.txt")
    # datetime型に変換
    latest_datetime = datetime.strptime(latest_time_req.text, "%Y-%m-%dT%H:%M:%S%z")
    time_yyyymmdd = latest_datetime.strftime('%Y%m%d') # 年月日　- アメダスデータ取得時に必要
    times_h3 = ("0" + str((latest_datetime.hour//3)*3))[-2:] # 3時間ごとの時間 - アメダスデータ取得時に必要

    # アメダスから気象データを取得して表示
    now_datas = get_amedas_data(OBSERV_POINT_NUM, time_yyyymmdd, times_h3)
    # 天気予報を取得して表示
    weather_forecast_text = get_weather_forecast(AREA_NUM, DETAIL_AREA_NUM)
    # 天気概況を取得して表示
    overview_forecast_text = get_overview_forecast(AREA_NUM)

    message = '#### 現在の気象データ\n'\
    '気温:' + now_datas['temp'] + '[℃]\n'\
    '湿度:' + now_datas['humidity'] + '[%]\n'\
    '気圧:' + now_datas['pressure'] + '[hPa]\n'\
    '降水量(10分毎):' + now_datas['prec10m'] + '[mm]\n\n'\
    '#### 明日の天気:\n'\
    + weather_forecast_text# + '\n\n'\
    #'#### 天気概況:\n'\
    #+ overview_forecast_text

    return message


LINE_NOTIFY_TOKEN= '取得したLINEのトークン'
url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ LINE_NOTIFY_TOKEN}

message = get_weather_datas()
payload = {"message" :  message}

r = requests.post(url ,headers = headers ,params=payload)
print(r)

