# products/models.py
from django.db import models

class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)          # 금융상품 코드
    kor_co_nm = models.TextField()                       # 금융회사명
    fin_prdt_nm = models.TextField()                     # 금융상품명
    etc_note = models.TextField()                        # 금융상품 설명
    join_deny = models.IntegerField()                    # 가입제한
    join_member = models.TextField()                     # 가입대상
    join_way = models.TextField()                        # 가입방법
    spcl_cnd = models.TextField()                        # 우대조건
    mtrt_int = models.TextField()                        # 만기 후 이자율


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()                     # 금융상품 코드
    intr_rate_type_nm = models.TextField()               # 금리유형
    intr_rate = models.FloatField(null=True)             # 금리
    intr_rate2 = models.FloatField(null=True)            # 최고우대금리
    save_trm = models.IntegerField(null=True)            # 저축기간

class DepositPopularity(models.Model):
    product = models.OneToOneField(
        DepositProducts, 
        on_delete=models.CASCADE, 
        related_name='popularity'
    )
    popularity = models.IntegerField(default=0)         # 인기도
    click_count = models.IntegerField(default=0)         # 클릭 수
    view_time_count = models.IntegerField(default=0)     # 페이지 머무른 횟수
    purchase_count = models.IntegerField(default=0)      # 구매 수

class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)          # 금융상품 코드
    kor_co_nm = models.TextField()                       # 금융회사명
    fin_prdt_nm = models.TextField()                     # 금융상품명
    etc_note = models.TextField()                        # 금융상품 설명
    join_deny = models.IntegerField()                    # 가입제한
    join_member = models.TextField()                     # 가입대상
    join_way = models.TextField()                        # 가입방법
    spcl_cnd = models.TextField()                        # 우대조건
    mtrt_int = models.TextField()                        # 만기 후 이자율

class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()                     # 금융상품 코드
    intr_rate_type_nm = models.TextField()               # 금리유형
    intr_rate = models.FloatField(null=True)             # 금리
    intr_rate2 = models.FloatField(null=True)            # 최고우대금리
    save_trm = models.IntegerField(null=True)            # 저축기간
    rsrv_type_nm = models.TextField()                    # 적립유형

class SavingPopularity(models.Model):
    product = models.OneToOneField(
        SavingProducts, 
        on_delete=models.CASCADE, 
        related_name='popularity'
    )
    popularity = models.IntegerField(default=0)         # 인기도
    click_count = models.IntegerField(default=0)         # 클릭 수
    view_time_count = models.IntegerField(default=0)     # 페이지 머무른 횟수
    purchase_count = models.IntegerField(default=0)      # 구매 수

