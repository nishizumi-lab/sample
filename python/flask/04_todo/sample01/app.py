from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
# データベースの設定(sqliteファイルのパスを指定)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite'
db = SQLAlchemy(app)


# Todoリストのモデルを定義(db.Modelクラスを継承する必要がある)
class Todo(db.Model):
    # テーブル名を設定(テーブル名はクラス名の複数形が一般的)
    __tablename__ = 'todos'
    # 作成するテーブルのカラムを定義
    # ID
    id = db.Column(db.Integer, primary_key=True)
    # コンテンツ
    content = db.Column(db.String(200), nullable=False)
    # 作成日
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


# ルートにアクセスされたらインデックページを開く
@app.route('/', methods=['POST', 'GET'])
def index():
    # POSTメソッドで要求されたら
    if request.method == 'POST':
        # コンテンツを取得
        task_content = request.form['content']
        # 新しいタスクを作成
        new_task = Todo(content=task_content)

        try:
            # データベースに新しいタスクを登録しトップページにリダイレクト
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "フォームの送信中に問題が発生しました"
    # 要求がない場合は、タスクリストを日付順に並べて表示
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# 削除画面
@app.route('/delete/<int:id>')
def delete(id):
    # 削除するタスクのIDを取得
    task_to_delete = Todo.query.get_or_404(id)

    try:
        # 削除対象のタスクをDBから削除しトップページにリダイレクト
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return '削除中に問題が発生しました'

# 編集画面
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def update(id):
    # 編集するタスクのIDを取得
    task_to_edit = Todo.query.get_or_404(id)
    # POSTメソッドがきたら編集対象のIDのコンテンツを更新
    if request.method == 'POST':
        task_to_edit.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "タスクの編集中に問題が発生しました"
    else:
        return render_template('edit.html', task=task_to_edit)


if __name__ == "__main__":
    # モデルからテーブルを作成(データベースファイルを最初に作るときだけ実行)
    #db.create_all()
    
    # アプリを起動(データベースファイルを最初に作るときはコメントアウトして実行しない)
    app.run(host="127.0.0.1", port=8080)
