from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # CSVファイルをPandasでロード
    df = pd.read_csv("https://raw.githubusercontent.com/nishizumi-lab/sample/master/python/flask/07_csv/00_sample_data/sample01.csv")

    # データフレームをリストに変換してテンプレートに渡す
    return render_template('index.html', title='価格推移', data_lists=df.values.tolist())

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
