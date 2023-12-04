from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TodosViewSetApiView, basename='todos_viewset')


urlpatterns = [
    path('', views.all_todos, name='all_todos'),
    path('<int:todo_id>', views.todo_detail_view, name='todo_detail_view'),
    path('cbv/', views.TodosListApiView.as_view(), name='all_todos'),
    path('cbv/<int:todo_id>', views.TodosDetailsApiView.as_view(), name='all_todos'),
    path('mixins/', views.TodosListMixinApiView.as_view(), name='all_todos'),
    path('mixins/<pk>', views.TodosDetailsMixinApiView.as_view(), name='all_todos'),
    path('generics/', views.TodosListGenericApiView.as_view(), name='all_todos'),
    path('generics/<pk>', views.TodosDetailsGenericApiView.as_view(), name='all_todos'),
    path('viewsets/',include(router.urls)),

]
