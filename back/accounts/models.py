# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.utils import user_email,user_username,user_field
# Create your models here.

# 필수 정보 : 이름
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True) # 별명
    name = models.CharField(max_length=50)   # 이름
    email = models.EmailField(max_length=100, blank=True, null=True)    # 이메일
    age = models.IntegerField(blank=True,null=True,default=0)   # 나이
    money = models.IntegerField(blank=True, null=True)  # 자산
    finance_product = models.JSONField(blank=True, null=True) # 가입 상품들
