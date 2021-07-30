from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import os
from datetime import datetime as dt
import pandas as pd

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
    date_fruit_list = pd.read_csv("./input/date_fruit.csv").values.tolist()

    return render_template('index.html', title='食べた果物記録', date_fruit_list=date_fruit_list)
## おまじない


if __name__ == '__main__':

    app.run(host="127.0.0.1", port=8080)
