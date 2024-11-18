from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegistrationView, name='register'),
    path('login/', views.UserLoginView, name='login'),
    path('logout/', views.UserLogoutView, name='logout'),
]
