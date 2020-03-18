# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def main():
    app.debug = True
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
