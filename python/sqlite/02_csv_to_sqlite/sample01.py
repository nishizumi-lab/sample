# -*- coding: utf-8 -*-
import csv
import sqlite3

csv_filepath = 'C:/github/sample/python/sqlite/00_sample_data/artoria.csv'
db_filepath = 'C:/github/sample/python/sqlite/00_sample_data/artoria.db'

# Connectionオブジェクトをメモリ上に作成してDBに接続
db = sqlite3.connect(db_filepath)
# Cursorオブジェクトを作成(DB上の処理対象の行を示す)
c = db.cursor()                

# artoriaという名前のtableを作成
c.execute("""CREATE TABLE artoria
 (name CHAR(15) NOT NULL,
 atk INTEGER NOT NULL,
 hp INTEGER NOT NULL);""")

# CSVをロードして中身をDBに挿入
with open(csv_filepath, 'r') as f: 
    b = csv.reader(f)
    header = next(b)
    for t in b:
        # tableに各行のデータを挿入
        c.execute('INSERT INTO artoria VALUES (?,?,?);', t)

# artoria tableの内容を表示
c.execute('SELECT * FROM artoria;')
print(c.fetchall()) 

# DBの変更を反映(コミット)
db.commit()

# DBとの接続を閉じる
db.close()