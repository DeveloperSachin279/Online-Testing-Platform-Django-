from django.urls import path # pyrefly: ignore [missing-import]
from . import views # pyrefly: ignore [missing-import]

urlpatterns = [
    path('', views.test_list, name='tests'),
    path('<slug:slug>/', views.test_details, name='test_details'),
    path('<slug:slug>/start/', views.start_test, name='start_test'),
    path('<slug:slug>/attempt/<int:attempt_id>/', views.test_attempt, name='test_attempt'),
    path('<slug:slug>/attempt/<int:attempt_id>/save_answer/', views.save_answer, name='save_answer'),
    path('<slug:slug>/attempt/<int:attempt_id>/submit/', views.submit_test, name='submit_test'),
]
