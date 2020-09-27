# -*- coding: utf-8
import sqlite3

# データベース開く
db = sqlite3.connect("C:/github/sample/python/sqlite/00_sample_data/sarvant.db")

c = db.cursor()
    
# テーブル作成
c.execute('create table artoria (name text, atk int, hp int)')

# コミット
db.commit()

# クローズ
db.close()
