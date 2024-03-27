from flask import Flask, render_template, url_for, request, redirect
# Blueprintをimportする
from flask import Blueprint

# Blueprintオブジェクトを生成
login_page = Blueprint('login', __name__)

# ログインページ
@login_page.route('/login')
def page1():
    message_hello = "ようこそ"
    return render_template('login.html',
                           message=message_hello)
