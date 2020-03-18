# coding: utf-8
from flask import Flask, render_template, url_for, request, redirect, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from apps import index, ini

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# ★分割先のコントローラー(Blueprint)を登録
app.register_blueprint(index.app)
app.register_blueprint(ini.app)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.debug = True  # デバッグモード有効化
    app.run(host="0.0.0.0", port=port)
