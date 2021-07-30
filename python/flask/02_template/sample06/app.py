from flask import Flask, render_template, url_for, request, redirect, Blueprint
import os
from apps import index, post, input_data # ★分割先をインポート

app = Flask(__name__)


# ★分割先のコントローラー(Blueprint)を登録
app.register_blueprint(index.app)
app.register_blueprint(post.app)
app.register_blueprint(input_data.app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.debug = True  # デバッグモード有効化
    app.run(host="0.0.0.0", port=port)
