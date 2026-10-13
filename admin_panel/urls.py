from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    
    path('subjects/', views.subject_list, name='admin_subject_list'),
    path('subjects/add/', views.subject_create, name='admin_subject_create'),
    path('subjects/<int:pk>/edit/', views.subject_update, name='admin_subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='admin_subject_delete'),
    
    path('exams/', views.exam_list, name='admin_exam_list'),
    path('exams/add/', views.exam_create, name='admin_exam_create'),
    path('exams/<int:pk>/', views.exam_detail, name='admin_exam_detail'),
    path('exams/<int:pk>/edit/', views.exam_update, name='admin_exam_update'),
    path('exams/<int:pk>/delete/', views.exam_delete, name='admin_exam_delete'),
    path('exams/<int:pk>/publish/', views.exam_publish_toggle, name='admin_exam_publish_toggle'),
    
    path('exams/<int:exam_id>/questions/add/', views.question_create, name='admin_question_create'),
    path('questions/<int:pk>/edit/', views.question_update, name='admin_question_update'),
    path('questions/<int:pk>/delete/', views.question_delete, name='admin_question_delete'),
    
    path('students/', views.student_list, name='admin_student_list'),
    path('students/<int:pk>/toggle/', views.student_toggle_active, name='admin_student_toggle_active'),
]
