# products/views.py
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import (
    DepositProductsSerializer, 
    DepositOptionsSerializer,
    SavingProductsSerializer, 
    SavingOptionsSerializer
)

API_KEY = settings.FIN_KEY
DEPOSIT_URL = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
SAVING_URL = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

@api_view(['GET'])
def save_products(request):
    # 예금상품 데이터 저장
    deposit_response = requests.get(DEPOSIT_URL).json()
    
    # 예금상품 기본정보 저장
    for product in deposit_response.get('result').get('baseList'):
        deposit_data = {
            'fin_prdt_cd': product.get('fin_prdt_cd'),
            'kor_co_nm': product.get('kor_co_nm'),
            'fin_prdt_nm': product.get('fin_prdt_nm'),
            'etc_note': product.get('etc_note'),
            'join_deny': int(product.get('join_deny')),
            'join_member': product.get('join_member'),
            'join_way': product.get('join_way'),
            'spcl_cnd': product.get('spcl_cnd'),
            'mtrt_int': product.get('mtrt_int'),
            'popularity': 0
        }
        serializer = DepositProductsSerializer(data=deposit_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # # 예금상품 옵션정보 저장
    # for option in deposit_response.get('result').get('optionList'):
    #     deposit_option_data = {
    #         'fin_prdt_cd': option.get('fin_prdt_cd'),
    #         'intr_rate_type_nm': option.get('intr_rate_type_nm'),
    #         'intr_rate': option.get('intr_rate'),
    #         'intr_rate2': option.get('intr_rate2'),
    #         'save_trm': int(option.get('save_trm'))
    #     }
    #     try:
    #         product = DepositProducts.objects.get(fin_prdt_cd=deposit_option_data['fin_prdt_cd'])
    #         serializer = DepositOptionsSerializer(data=deposit_option_data)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save(product=product)
    #     except DepositProducts.DoesNotExist:
    #         continue
    for option in deposit_response.get('result').get('optionList'):
        try:
            product = DepositProducts.objects.get(fin_prdt_cd=option.get('fin_prdt_cd'))
            DepositOptions.objects.create(
                product=product,
                fin_prdt_cd=option.get('fin_prdt_cd'),
                intr_rate_type_nm=option.get('intr_rate_type_nm'),
                intr_rate=option.get('intr_rate'),
                intr_rate2=option.get('intr_rate2'),
                save_trm=int(option.get('save_trm'))
            )
        except DepositProducts.DoesNotExist:
            continue

    # 적금상품 데이터 저장
    saving_response = requests.get(SAVING_URL).json()
    
    # 적금상품 기본정보 저장
    for product in saving_response.get('result').get('baseList'):
        saving_data = {
            'fin_prdt_cd': product.get('fin_prdt_cd'),
            'kor_co_nm': product.get('kor_co_nm'),
            'fin_prdt_nm': product.get('fin_prdt_nm'),
            'etc_note': product.get('etc_note'),
            'join_deny': int(product.get('join_deny')),
            'join_member': product.get('join_member'),
            'join_way': product.get('join_way'),
            'spcl_cnd': product.get('spcl_cnd'),
            'mtrt_int': product.get('mtrt_int'),
            'popularity': 0
        }
        serializer = SavingProductsSerializer(data=saving_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # # 적금상품 옵션정보 저장
    # for option in saving_response.get('result').get('optionList'):
    #     saving_option_data = {
    #         'fin_prdt_cd': option.get('fin_prdt_cd'),
    #         'intr_rate_type_nm': option.get('intr_rate_type_nm'),
    #         'intr_rate': option.get('intr_rate'),
    #         'intr_rate2': option.get('intr_rate2'),
    #         'save_trm': int(option.get('save_trm')),
    #         'rsrv_type_nm': option.get('rsrv_type_nm', '')
    #     }
    #     try:
    #         product = SavingProducts.objects.get(fin_prdt_cd=saving_option_data['fin_prdt_cd'])
    #         serializer = SavingOptionsSerializer(data=saving_option_data)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save(product=product)
    #     except SavingProducts.DoesNotExist:
    #         continue
    for option in saving_response.get('result').get('optionList'):
        try:
            product = SavingProducts.objects.get(fin_prdt_cd=option.get('fin_prdt_cd'))
            SavingOptions.objects.create(
                product=product,
                fin_prdt_cd=option.get('fin_prdt_cd'),
                intr_rate_type_nm=option.get('intr_rate_type_nm'),
                intr_rate=option.get('intr_rate'),
                intr_rate2=option.get('intr_rate2'),
                save_trm=int(option.get('save_trm')),
                rsrv_type_nm=option.get('rsrv_type_nm', '')  # 적금 옵션에만 있는 필드
            )
        except SavingProducts.DoesNotExist:
            continue

    return Response({'message': '데이터 저장이 완료되었습니다.'}, status=status.HTTP_201_CREATED)