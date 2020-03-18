from django.db import models 

"""
ToDOモデルは、ToDo(todo)、作成日時(created_at)、更新日時(updated_at)の属性を持つ
"""
 
class Todo(models.Model): 
    todo = models.CharField('ToDo', max_length=100, blank=False)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)
    
    def __str__(self):
        return self.todo
