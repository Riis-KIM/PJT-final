from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('save/', views.save_products, name='save_products'),
]
