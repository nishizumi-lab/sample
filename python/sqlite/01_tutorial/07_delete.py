# -*- coding: utf-8
import sqlite3

# データベース開く
db = sqlite3.connect("C:/github/sample/python/sqlite/00_sample_data/sarvant.db")
c = db.cursor()

# データ更新
# artoriaテーブルのnameが「artoria santa alter」のレコードを削除
sql = 'DELETE FROM artoria where name = "artoria santa alter"'
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
('mystery heroine xx', 11761, 12696)
('mystery heroine x alter', 11113, 14175)
"""