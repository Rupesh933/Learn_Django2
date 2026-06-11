from django.urls import path
from . import views

app_name = 'to_do_app'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),

    # Toggle task completion status 
    path('toggle/<int:pk>/', views.toggle_task, name='toggle_task'),
]