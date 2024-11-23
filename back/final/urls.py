from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('products.urls')),
    path('accounts/custom/', include('accounts.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path(
        'password-reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('exchange/', include('exchange.urls')),
    path('articles/', include('articles.urls')),
]