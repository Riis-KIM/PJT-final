# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import DepositProducts, SavingProducts

# Create your models here.

# 필수 정보 : 이름
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True) # 별명
    name = models.CharField(max_length=50)   # 이름
    email = models.EmailField(max_length=100, blank=True, null=True)    # 이메일
    age = models.IntegerField(blank=True,null=True,default=0)   # 나이
    money = models.IntegerField(blank=True, null=True)  # 자산
    joined_deposits = models.ManyToManyField(
        DepositProducts, 
        related_name='joined_users',
        blank=True
    )  # 가입한 예금상품
    joined_savings = models.ManyToManyField(
        SavingProducts,
        related_name='joined_users',
        blank=True
    )  # 가입한 적금상품
