# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('myproducts/', views.my_products, name='my_products'),  # 가입한 상품 목록 조회만 남김
]