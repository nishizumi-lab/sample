from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import pandas as pd
import os
from datetime import datetime as dt

app = Flask(__name__, static_url_path="")

# 処理した画像ファイルの保存先
IMG_DIR = "/static/images/"
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = BASE_DIR + IMG_DIR

# 保存先のパスがなければ作成
if not os.path.isdir(IMG_PATH):
    os.mkdir(IMG_PATH)



@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                    'B': [5, 6, 7, 8, 9],
                    'C': ['a', 'b', 'c--', 'd', 'e']})
    
    if request.method == 'POST':
        # 画像をロード
        csv_data = request.files['csv']
        df = pd.read_csv(csv_data)

        # 画像データ用配列にデータがあれば
        print(df)


    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)
