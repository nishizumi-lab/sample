# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<html><span style="color:#ff0000;">Hello World</span></html>'


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)
