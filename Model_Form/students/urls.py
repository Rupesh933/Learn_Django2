from django.urls import path
from .views import student_create, student_list, student_details, student_edit, student_delete

urlpatterns = [
    path('add/', student_create, name='student_create'),
    path('', student_list, name='student_list'),
    path('student_details/<int:pk>/', student_details, name='student_details'),
    path('student_edit/<int:pk>/', student_edit, name='student_edit'),
    path('student_delete/<int:pk>/', student_delete, name='student_delete')
]
