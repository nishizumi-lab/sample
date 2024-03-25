# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    # クライアントに以下の文字列(HTML)を返す
    return '<html><br><br>トップページです</html>'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug = True)
    
    
