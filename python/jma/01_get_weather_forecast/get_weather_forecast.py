# -*- coding:utf-8 -*-
import requests

# 気象庁から天気予報情報(JSONデータ)を取得
# ファイルパスの「280000」はエリアコード。取得したい地域に応じて適宜変更します。
JSON_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
jma_json = requests.get(JSON_URL).json()

print(jma_json)
