from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('save/', views.save_products, name='save_products'),
    path('deposits/', views.deposit_list, name='deposit_list'),
    path('savings/', views.saving_list, name='saving_list'),
    # path('deposits/<str:fin_prdt_cd>/', views.deposit_detail, name='saving_detail'),
    # path('savings/<str:fin_prdt_cd>/', views.saving_detail, name='saving_detail'),
]
