from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_todos, name='all_todos'),
    path('<int:todo_id>', views.todo_detail_view, name='todo_detail_view'),
    path('cbv/', views.TodosListApiView.as_view(), name='all_todos'),
    path('cbv/<int:todo_id>', views.TodosDetailsApiView.as_view(), name='all_todos'),
]
