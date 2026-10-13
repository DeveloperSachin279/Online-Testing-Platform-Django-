from django.urls import path # pyrefly: ignore [missing-import] 
from django.contrib.auth import views as auth_views # pyrefly: ignore [missing-import]
from . import views # pyrefly: ignore [missing-import]

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html', 
        redirect_authenticated_user=True,
        extra_context={'public_page': True}
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
