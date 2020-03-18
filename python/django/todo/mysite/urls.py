from django.contrib import admin
from django.urls import include, path   # includeをimport
"""
ユーザーがアクセスするURL（http://www.example.jp/など）と、
urlpatternsに格納したすべてのpath()の初めの引数（'admin/'や'index/'）を順番に比較し、
URLと引数が一致した場合、path()の2つ目の引数（admin.site.urlsやinclude()など）を利用する
"""

urlpatterns = [
    # todo/でアクセスした際はtodoのurl設定を参照
    path('todo/', include('todo.urls')),
    
    # URLが「admin/」の場合、管理画面（admin.site.urls）を返す（ブラウザに表示する）
    path('admin/', admin.site.urls),


    #path('index/', include('mysite.urls', namespace='mysite')),
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
