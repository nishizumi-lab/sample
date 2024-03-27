from flask import Flask, render_template, url_for, request, redirect
from flask import Blueprint # Blueprintをインポート

# 関数名(index)でBlueprintオブジェクトを生成
index_app = Blueprint('index', __name__)

@index_app.route('/')
def index():
    name = "トップページ"
    message = "トップページのメッセージ"

    return render_template('index.html',
                           message=message, name=name)
