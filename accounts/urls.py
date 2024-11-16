# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
path('profile/edit/', views.edit_profile_view, name='edit_profile'),  # Маршрут для редагування профілю
    path('delete/', views.delete_account_view, name='delete_account'),
]
