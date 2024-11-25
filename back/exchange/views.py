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
    exchange_response = requests.get(EXCHANGE_URL, params, verify=False)
    
    if exchange_response.status_code == 200:
        return Response(exchange_response.json(), status=status.HTTP_200_OK)
    
    return Response({'error': 'Failed to fetch exchange rate data'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def get_market_data(request):
#     try:
#         # User-Agent 헤더 추가
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         # KOSPI 데이터 가져오기
#         kospi_url = 'https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11'
#         kospi_response = requests.get(kospi_url, headers=headers)
#         kospi_data = kospi_response.json()['chart']['result'][0]['meta']
        
#         # NASDAQ 데이터 가져오기
#         nasdaq_url = 'https://query1.finance.yahoo.com/v8/finance/chart/%5EIXIC'
#         nasdaq_response = requests.get(nasdaq_url, headers=headers)
#         nasdaq_data = nasdaq_response.json()['chart']['result'][0]['meta']
        
#         # 데이터 가공
#         market_data = {
#             'kospi': {
#                 'price': round(kospi_data['regularMarketPrice'], 2),
#                 'change': round(((kospi_data['regularMarketPrice'] - kospi_data['chartPreviousClose']) / 
#                                kospi_data['chartPreviousClose'] * 100), 2)
#             },
#             'nasdaq': {
#                 'price': round(nasdaq_data['regularMarketPrice'], 2),
#                 'change': round(((nasdaq_data['regularMarketPrice'] - nasdaq_data['chartPreviousClose']) / 
#                                 nasdaq_data['chartPreviousClose'] * 100), 2)
#             }
#         }
        
#         return Response(market_data)
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)

import yfinance as yf
from datetime import datetime, timedelta
@api_view(['GET'])
def get_market_data(request):
    try:
        # User-Agent 헤더 추가
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # KOSPI 데이터 가져오기
        kospi_ticker = yf.Ticker('^KS11')
        kospi_data = kospi_ticker.history(period='1mo')
        
        # NASDAQ 데이터 가져오기
        nasdaq_ticker = yf.Ticker('^IXIC')
        nasdaq_data = nasdaq_ticker.history(period='1mo')
        
        # 데이터 가공
        market_data = {
            'kospi': {
                'price': round(kospi_data['Close'][-1], 2),
                'change': round(((kospi_data['Close'][-1] - kospi_data['Close'][-2]) / kospi_data['Close'][-2] * 100), 2),
                'last_1_month': kospi_data['Close'].tolist()
            },
            'nasdaq': {
                'price': round(nasdaq_data['Close'][-1], 2),
                'change': round(((nasdaq_data['Close'][-1] - nasdaq_data['Close'][-2]) / nasdaq_data['Close'][-2] * 100), 2),
                'last_1_month': nasdaq_data['Close'].tolist()
            }
        }
        return Response(market_data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)