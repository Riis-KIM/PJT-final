from django.urls import path
from . import views
app_name = 'exchange'

urlpatterns = [
    path('', views.exchange_info, name='exchange_info'),
]
