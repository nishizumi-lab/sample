from django.urls import path
from . import views 
 
app_name = 'todo' 

"""
ユーザーがアクセスするURL（http://www.example.jp/list/）と、
urlpatternsに格納したすべてのpath()の初めの引数（'admin/'や'index/'）を順番に比較し、
URLと引数が一致した場合、path()の2つ目の引数（views.TodoListView.as_view()など）を利用する
"""

urlpatterns = [
    # 「list」のようなURLのとき、todo/views.pyのTodoListVIewを利用
    path('list/', views.TodoListView.as_view(), name='list'),

    # 「detail/123」（123はint：整数）のようなURLのとき、todo/views.pyのTodoDetailVIewを利用
    path('detail/<int:pk>/', views.TodoDetailView.as_view(), name='detail'), 
    path('create/', views.TodoCreateView.as_view(), name='create'), 
    path('update/<int:pk>/', views.TodoUpdateView.as_view(), name='update'), 
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='delete'), 
]

"""
【path関数】
第一引数：URL
第二引数：URLに対応するview関数
（クラスベースの場合、viewクラス名でas_viewメソッドを呼び出す）
name引数：テンプレート内で指定するURLの名称
（省略するとview関数の名前がそのまま利用される）

【include関数】
path関数の第二引数にview関数の代わりに指定する事でURLを連結
path("", include("todo.urls"))
※上の例ではtodo.urls.pyで設定したURLを連結
"""
