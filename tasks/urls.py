from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = "tasks"

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.TaskListView.as_view(), name='list'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('list/complete/<int:uid>', views.complete_task, name='complete'),
    path('list/delete/<int:uid>', views.delete_task, name='delete'),
    path('details/<int:pk>', views.TaskDetailsView.as_view(), name='details'),
    path('edit/<int:pk>', views.TaskEditView.as_view(), name='edit'),
    path('export/', views.TaskExportView.as_view(), name='export'),
]
