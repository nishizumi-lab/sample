import os
import csv

# ロードするCSVファイルのパスと文字コード
load_csv_path = "C:/github/sample/python/file/03_csv/00_sample_data/class_list.csv"
encode_type = "UTF-8"

# ディレクトリを自動生成する先のパス
make_dir_path = "C:/github/sample/python/file/03_csv/01_list_to_dir/"

with open(load_csv_path, encoding = encode_type) as f:
    # CSVファイルをロード
    reader = csv.reader(f)
    # 1行ずつデータを取り出し
    for row in reader:
        # 1列目（管理番号）と2列目（クラス名）をディレクトリ名にする
        dir_name = row[0] + '-' + row[1]
        # ディレクトリがなければ新規作成
        if not os.path.exists(make_dir_path + dir_name):
            os.mkdir(make_dir_path + dir_name)

"""
C:/github/sample/python/file/03_csv/01_list_to_dir/内に以下のディレクトリが作成されます。

1-A組
2-B組
3-C組
4-D組
5-E組
"""