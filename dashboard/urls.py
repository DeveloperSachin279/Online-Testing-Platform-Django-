from django.urls import path # pyrefly: ignore [missing-import]
from . import views # pyrefly: ignore [missing-import]

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
