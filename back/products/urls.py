from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('save/', views.save_products, name='save_products'),
    path('deposits/', views.deposit_list, name='deposit_list'),
    path('savings/', views.saving_list, name='saving_list'),
    path('deposits/<str:fin_prdt_cd>/join/', views.deposit_join, name='deposit_join'),
    path('savings/<str:fin_prdt_cd>/join/', views.saving_join, name='saving_join'),
]
