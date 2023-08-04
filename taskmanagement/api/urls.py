from django.urls import path
from .views import (
    BoardListView, BoardDetailView,
    BoardUpdateView, BoardDeleteView,
    ColumnCreateView, ColumnDeleteView,
    TaskCreateView, ColumnListView,
    TaskDetailView, TaskUpdateView,
    TaskDeleteView, BoardCreateView,
    SubtaskCreateView, SubtaskDeleteView,
    SubtaskUpdateView
)

urlpatterns = [
    # board
    path('boards/', BoardListView.as_view(), name='board_list'),
    path('boards/create/', BoardCreateView.as_view(), name='board_create'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('boards/<int:pk>/update/', BoardUpdateView.as_view(), name='board_update'),
    path('boards/<int:pk>/delete/', BoardDeleteView.as_view(), name='board_delete'),
    # column
    path('boards/<int:board_pk>/columns/', ColumnListView.as_view(), name='column_list'),
    path('boards/<int:board_pk>/add_column/', ColumnCreateView.as_view(), name='column_create'),
    path('columns/<int:pk>/delete/', ColumnDeleteView.as_view(), name='column_delete'),
    # task
    path('boards/<int:board_pk>/add_task/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    # subtask
    path('tasks/<int:task_pk>/add_subtask/', SubtaskCreateView.as_view(), name='subtask_create'),
    path('subtasks/<int:pk>/update/', SubtaskUpdateView.as_view(), name='subtask_update'),
    path('subtasks/<int:pk>/delete/', SubtaskDeleteView.as_view(), name='subtask_delete')
]