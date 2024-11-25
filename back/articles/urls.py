# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    # 게시글 관련 URL
    path('', views.article_list_create, name='article_list_create'),
    path('<int:article_pk>/', views.article_detail_update_delete, name='article_detail_update_delete'),
    path('<int:article_pk>/like/', views.article_like),
    path('<int:article_pk>/views/', views.article_views),
    
    # 댓글 관련 URL
    path('<int:article_pk>/comments/', views.comment_create_delete, name='comment_create'),
    path('<int:article_pk>/comments/<int:comment_pk>/', views.comment_create_delete, name='comment_delete'),
    path('<int:article_pk>/comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
]