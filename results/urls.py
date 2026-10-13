from django.urls import path
from . import views

urlpatterns = [
    path('', views.result_list, name='results'),
    path('attempt/<slug:slug>/<int:attempt_id>/', views.attempt_summary, name='attempt_summary'),
    path('<int:attempt_id>/', views.detailed_result, name='detailed_result'),
]
