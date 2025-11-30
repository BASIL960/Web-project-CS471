from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'), # [cite: 63]
    path('login/', views.login_user, name='login_user'),          # [cite: 64]
    path('logout/', views.logout_user, name='logout_user'),       # 
]