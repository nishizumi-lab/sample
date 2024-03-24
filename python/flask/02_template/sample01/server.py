# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect
import time, datetime

app = Flask(__name__)

@app.route('/')
def index():
    message_hello = "■■■■■■■■■■Hello World!■■■■■■■■■■■"

    # index.htmlの変数展開(message_helloの値がHTMLのmessageに渡される)
    return render_template('index.html',
                           message=message_hello)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)