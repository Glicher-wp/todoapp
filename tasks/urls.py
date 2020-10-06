from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = "tasks"

urlpatterns = [
    path('', views.index, name='index'),
    #path('list/', views.TaskListView.as_view(), name='list'),
    path('list/', views.tasks_by_tag, name='list'),
    path('list/tag/<slug:tag_slug>', views.tasks_by_tag, name='list_by_tag'),
    path('list/uncompleted/', views.TaskListUncompleted.as_view(), name="uncompleted"),
    path('list/grouped/', views.TaskListGrouped.as_view(), name="grouped"),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('list/complete/<int:uid>', views.complete_task, name='complete'),
    path('list/delete/<int:uid>', views.delete_task, name='delete'),
    path('list/tag/<slug:tag_slug>/delete/<int:uid>', views.delete_task, name='delete_tag_list'),
    path('details/<int:pk>', views.TaskDetailsView.as_view(), name='details'),
    path('edit/<int:pk>', views.TaskEditView.as_view(), name='edit'),
    path('import/', views.TaskImportView.as_view(), name='import'),
    path('export/', views.TaskExportView.as_view(), name='export'),
    path('bugtest/', views.zero_devision_test)
]
