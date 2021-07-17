from flask import Flask, render_template, url_for, request, redirect
# Blueprintをimportする
from flask import Blueprint

# 関数名(page1)でBlueprintオブジェクトを生成
page1_app = Blueprint('page1', __name__)

# ページ1
@page1_app.route('/page1')
def page1():
    name = "ページ1"
    message = "ページ1のメッセージ"

    # 変数展開(messageとnameの値がHTMLに渡される)
    return render_template('page1.html',
                           message=message, name=name)
