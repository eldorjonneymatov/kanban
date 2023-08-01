from django.contrib import admin
from .models import Board, Column, Task, Subtask

admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Task)
admin.site.register(Subtask)