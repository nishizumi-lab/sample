# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    message_hello = "こんにちは"
    return render_template('index.html',
                           message=message_hello)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug = True)