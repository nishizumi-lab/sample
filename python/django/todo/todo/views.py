from django.views import generic
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm

# Djangoで予め用意されているListView, DetailView, CreateView, UpdateView, DeleteViewを利用

# 一覧表示
class TodoListView(generic.ListView):
    """
    テンプレートを指定しないと、「モデル名_list.html」が使用される
    また、自動でページネーションも自動でやってくれる
    """
    model = Todo
    paginate_by = 5 # ページネーションが5ページまで

# 詳細表示
class TodoDetailView(generic.DetailView):
    """
    Todoの詳細表示
    テンプレートを指定しないと「モデル名_detail.html」が使用される
    """
    model = Todo

# 新規作成
class TodoCreateView(generic.CreateView):
    """
    Todoの新規作成
    テンプレートを指定しないと「モデル名_form.html」が使用される
    """
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy('todo:list')

# 更新
class TodoUpdateView(generic.UpdateView):
    """
    Todoの新規作成
    テンプレートを指定しないと「モデル名_form.html」が使用される
    """
    model = Todo
    form_class = TodoForm
    success_url = reverse_lazy('todo:list')

# 削除
class TodoDeleteView(generic.DeleteView):
    """
    Todoの削除
    テンプレートを指定しないと「モデル名_confirm_delete.html」が使用される
    【デフォルトの動作】
    getリクエスト・・・確認ページへ遷移
    postリクエスト・・・削除を実行
    【補足】
    レコードを削除せず、有効フラグを消す(論理削除)場合は
    deleteをオーバーライドしてその中に処理を書く
    """
    model = Todo
    success_url = reverse_lazy('todo:list')
