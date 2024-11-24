# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('myproducts/', views.my_products, name='my_products'),  # 가입한 상품 목록 조회만 남김
    path('check-email/', views.check_email, name='check_email'),    # 가입한 이메일인지 확인함
]