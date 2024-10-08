# -*- coding:utf-8 -*-
import requests

# 気象庁から天気予報情報(JSONデータ)を取得
# ファイルパスの「270000」はエリアコード。取得したい地域に応じて適宜変更します。
JSON_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
jma_json = requests.get(JSON_URL).json()

print(jma_json)

"""
[
	{
		"publishingOffice": "大阪管区気象台",
		"reportDatetime": "2024-03-16T05:00:00+09:00",
		"timeSeries": [
			{
				"timeDefines": [
					"2024-03-16T05:00:00+09:00",
					"2024-03-17T00:00:00+09:00"
				],
				"areas": [
					{
						"area": {
							"name": "大阪府",
							"code": "270000"
						},
						"weatherCodes": [
							"100",
							"212"
						],
						"weathers": [
							"晴れ",
							"晴れ　後　くもり　夕方　一時　雨"
						],
						"winds": [
							"北東の風　後　北の風",
							"北の風　日中　南西の風　海上　では　後　北の風　やや強く"
						],
						"waves": [
							"０．５メートル",
							"０．５メートル　後　１メートル"
						]
					}
				]
			},
			{
				"timeDefines": [
					"2024-03-16T06:00:00+09:00",
					"2024-03-16T12:00:00+09:00",
					"2024-03-16T18:00:00+09:00",
					"2024-03-17T00:00:00+09:00",
					"2024-03-17T06:00:00+09:00",
					"2024-03-17T12:00:00+09:00",
					"2024-03-17T18:00:00+09:00"
				],
				"areas": [
					{
						"area": {
							"name": "大阪府",
							"code": "270000"
						},
						"pops": [
							"0",
							"0",
							"0",
							"0",
							"10",
							"50",
							"30"
						]
					}
				]
			},
			{
				"timeDefines": [
					"2024-03-16T09:00:00+09:00",
					"2024-03-16T00:00:00+09:00",
					"2024-03-17T00:00:00+09:00",
					"2024-03-17T09:00:00+09:00"
				],
				"areas": [
					{
						"area": {
							"name": "大阪",
							"code": "62078"
						},
						"temps": [
							"19",
							"19",
							"8",
							"17"
						]
					}
				]
			}
		]
	},
	{
		"publishingOffice": "大阪管区気象台",
		"reportDatetime": "2024-03-15T17:00:00+09:00",
		"timeSeries": [
			{
				"timeDefines": [
					"2024-03-16T00:00:00+09:00",
					"2024-03-17T00:00:00+09:00",
					"2024-03-18T00:00:00+09:00",
					"2024-03-19T00:00:00+09:00",
					"2024-03-20T00:00:00+09:00",
					"2024-03-21T00:00:00+09:00",
					"2024-03-22T00:00:00+09:00"
				],
				"areas": [
					{
						"area": {
							"name": "大阪府",
							"code": "270000"
						},
						"weatherCodes": [
							"100",
							"112",
							"101",
							"201",
							"202",
							"201",
							"101"
						],
						"pops": [
							"",
							"50",
							"20",
							"30",
							"50",
							"30",
							"20"
						],
						"reliabilities": [
							"",
							"",
							"A",
							"A",
							"C",
							"A",
							"A"
						]
					}
				]
			},
			{
				"timeDefines": [
					"2024-03-16T00:00:00+09:00",
					"2024-03-17T00:00:00+09:00",
					"2024-03-18T00:00:00+09:00",
					"2024-03-19T00:00:00+09:00",
					"2024-03-20T00:00:00+09:00",
					"2024-03-21T00:00:00+09:00",
					"2024-03-22T00:00:00+09:00"
				],
				"areas": [
					{
						"area": {
							"name": "大阪",
							"code": "62078"
						},
						"tempsMin": [
							"",
							"8",
							"6",
							"4",
							"4",
							"3",
							"4"
						],
						"tempsMinUpper": [
							"",
							"10",
							"7",
							"6",
							"5",
							"5",
							"6"
						],
						"tempsMinLower": [
							"",
							"6",
							"5",
							"3",
							"2",
							"2",
							"2"
						],
						"tempsMax": [
							"",
							"17",
							"13",
							"14",
							"11",
							"11",
							"14"
						],
						"tempsMaxUpper": [
							"",
							"19",
							"14",
							"17",
							"14",
							"14",
							"17"
						],
						"tempsMaxLower": [
							"",
							"16",
							"11",
							"13",
							"10",
							"8",
							"11"
						]
					}
				]
			}
		],
		"tempAverage": {
			"areas": [
				{
					"area": {
						"name": "大阪",
						"code": "62078"
					},
					"min": "6.2",
					"max": "14.7"
				}
			]
		},
		"precipAverage": {
			"areas": [
				{
					"area": {
						"name": "大阪",
						"code": "62078"
					},
					"min": "13.7",
					"max": "31.5"
				}
			]
		}
	}
]
"""
