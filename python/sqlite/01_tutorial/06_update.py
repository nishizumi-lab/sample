# -*- coding: utf-8
import sqlite3

# データベース開く
db = sqlite3.connect("C:/github/sample/python/sqlite/00_sample_data/sarvant.db")
c = db.cursor()

# データ更新
# artoriaテーブルのnameカラムにあるmystery heroine xをmystery heroine xxに更新
sql = 'UPDATE artoria SET name = "mystery heroine xx" where name = "mystery heroine x"'
c.execute(sql)

# コミット
db.commit()

# データ（レコード）取得
sql = 'select * from artoria'
for row in c.execute(sql):
    print(row)

# クローズ
db.close() 

"""
('artoria', 11221, 15150)
('artoria alter', 10248, 11589)
('artoria lily', 7726, 10623)
('artoria lancer', 10995, 15606)
('artoria lancer alter', 9968, 11761)
('artoria swimwear', 11276, 14553)
('artoria santa alter', 9258, 11286)
('mystery heroine xx', 11761, 12696)
('mystery heroine x alter', 11113, 14175)
"""