# -*- coding: utf-8 -*-
import sqlite3

# DBに接続
db = sqlite3.connect("C:/github/sample/python/sqlite/00_sample_data/sarvant.db")

# DB閉じる
db.close()