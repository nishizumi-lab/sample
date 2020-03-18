from django.contrib import admin
from django.urls import include, path   # includeをimport

urlpatterns = [
    path('todo/', include('todo.urls')),    # todo/でアクセスした際はtodoのurl設定を参照させる
    path('admin/', admin.site.urls),
]
