from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

EXCHANGE_URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
API_KEY = settings.EXC_KEY

@api_view(['GET'])
def exchange_info(request):

    params={
        'authkey': API_KEY,
        'searchdate': '20241119',
        'data': 'AP01',
    }
    exchange_response = requests.get(EXCHANGE_URL, params)
    
    if exchange_response.status_code == 200:
        return Response(exchange_response.json(), status=status.HTTP_200_OK)
    
    return Response({'error': 'Failed to fetch exchange rate data'}, status=status.HTTP_400_BAD_REQUEST)