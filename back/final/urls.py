from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('products.urls')),
    path('accounts/custom/', include('accounts.urls')),  # 유저의 상품 가입 정보를 얻기 위한 정보
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('exchange/', include('exchange.urls')),
    path('articles/', include('articles.urls')),
]
