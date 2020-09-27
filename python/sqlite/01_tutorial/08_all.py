# -*- coding: utf-8
import sqlite3

# データベースを開く
# ファイルがなければ新規作成
db = sqlite3.connect("C:/github/sample/python/sqlite/00_sample_data/sarvant.db")

c = db.cursor()

# テーブル作成
c.execute('create table artoria (name text, atk int, hp int)')

# データ追加(レコード登録)
sql = 'insert into artoria (name, atk, hp) values (?,?,?)'
data = [('artoria',11221,15150),
            ('artoria alter',10248,11589),
            ('artoria lily', 7726,10623),
            ('artoria lancer',10995,15606),
            ('artoria lancer alter',9968,11761),
            ('artoria swimwear',11276,14553),
            ('artoria santa alter',9258,11286),
            ('mystery heroine x',11761,12696),
            ('mystery heroine x alter',11113,14175)]

c.executemany(sql, data)

# コミット（変更を確定する）
db.commit()
    
# データ（レコード）を取得して表示
sql = 'select * from artoria'
print("---------------------")
for row in c.execute(sql):
    print(row)

"""
('artoria', 11221, 15150)
('artoria alter', 10248, 11589)
('artoria lily', 7726, 10623)
('artoria lancer', 10995, 15606)
('artoria lancer alter', 9968, 11761)
('artoria swimwear', 11276, 14553)
('artoria santa alter', 9258, 11286)
('mystery heroine x', 11761, 12696)
('mystery heroine x alter', 11113, 14175)
"""

# データ追加(1つのレコードを登録)
sql = 'insert into artoria (name, atk, hp) values (?,?,?)'
data = ('artoria caster', 15341, 11230)
c.execute(sql, data)

# コミット（変更を確定する）
db.commit()

# データ（レコード）を取得して表示
print("---------------------")
sql = 'select * from artoria'
for row in c.execute(sql):
    print(row)
"""
('artoria', 11221, 15150)
('artoria alter', 10248, 11589)
('artoria lily', 7726, 10623)
('artoria lancer', 10995, 15606)
('artoria lancer alter', 9968, 11761)
('artoria swimwear', 11276, 14553)
('artoria santa alter', 9258, 11286)
('mystery heroine x', 11761, 12696)
('mystery heroine x alter', 11113, 14175)
('artoria caster', 15341, 11230)
"""


# データ更新
# artoriaテーブルのnameカラムにあるartoria casterをcastriaに更新
sql = 'UPDATE artoria SET name = "artoria caster" where name = "castria"'
c.execute(sql)

# コミット（変更を確定する）
db.commit()

# データ（レコード）を取得して表示
print("---------------------")
sql = 'select * from artoria'
for row in c.execute(sql):
    print(row)
"""
('artoria', 11221, 15150)
('artoria alter', 10248, 11589)
('artoria lily', 7726, 10623)
('artoria lancer', 10995, 15606)
('artoria lancer alter', 9968, 11761)
('artoria swimwear', 11276, 14553)
('artoria santa alter', 9258, 11286)
('mystery heroine x', 11761, 12696)
('mystery heroine x alter', 11113, 14175)
('artoria caster', 15341, 11230)
"""


# データ削除
# artoriaテーブルのnameが「castria」のレコードを削除
sql = 'DELETE FROM artoria where name = "castria"'
c.execute(sql)

# コミット（変更を確定する）
db.commit()

# データ（レコード）を取得して表示
print("---------------------")
sql = 'select * from artoria'
for row in c.execute(sql):
    print(row)

"""
('artoria', 11221, 15150)
('artoria alter', 10248, 11589)
('artoria lily', 7726, 10623)
('artoria lancer', 10995, 15606)
('artoria lancer alter', 9968, 11761)
('artoria swimwear', 11276, 14553)
('artoria santa alter', 9258, 11286)
('mystery heroine x', 11761, 12696)
('mystery heroine x alter', 11113, 14175)
('artoria caster', 15341, 11230)
"""

# クローズ
db.close() 
