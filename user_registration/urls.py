from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='user_registration/login.html'), name='login'),

    # Logout URL
        path('logout/', LogoutView.as_view(template_name='user_registration/logout.html'), name='logout'),    ]

