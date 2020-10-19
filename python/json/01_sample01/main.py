
# -*- coding:utf-8 -*-
import json
import codecs

# ① JSON ファイルの読み込み
f = codecs.open("C:/github/sample/python/json/01_sample01/data.json", encoding="utf-8")
json_data = json.load(f)
f.close()

print(json_data)
# {'西住': {'height': 158, 'position': '車長'}, '秋山': {'height': 157, 'position': '装填手'}}

print(type(json_data))
# <class 'dict'>


# ② 特定のデータを取りだす
print(json_data["西住"]) # {'height': 158, 'position': '車長'}
print(json_data["秋山"]) # {'height': 157, 'position': '装填手'}



# ③ JSON ファイルの書き込み
# 空の辞書を作成
data = {}

# 辞書にデータを挿入
data["西住"] = {"height": 158 , "position": "車長"}
data["秋山"] = {"height": 157 , "position": "装填手"}

# JSONファイルに出力
with codecs.open('C:/github/sample/python/json/01_sample01/data2.json', 'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

"""
data2.jsonの中身

{
    "西住": {
        "height": 158,
        "position": "車長"
    },
    "秋山": {
        "height": 157,
        "position": "装填手"
    }
}

"""
