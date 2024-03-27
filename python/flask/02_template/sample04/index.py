from flask import Flask, render_template, url_for, request, redirect
from flask import Blueprint # Blueprintをインポート

# Blueprintオブジェクトを生成
index_page = Blueprint('index', __name__)

# トップページ
@index_page.route('/')
def index():
    message_hello= "ようこそ"

    return render_template('index.html',
                           message=message_hello)
