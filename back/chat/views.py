# chat/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import openai

@api_view(['POST'])
def chat_with_gpt(request):
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        user_message = request.data.get('message', '')
        
        response = client.chat.completions.create(
            model="gpt4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 금융 상품 추천 및 상담 전문가입니다. 다음 원칙을 준수하여 응답해주세요:

                    1. 기본 응대 원칙:
                    - 친절하고 전문적인 어조 유지
                    - 금융 용어는 쉽게 설명
                    - 객관적이고 정확한 정보 제공
                    - 법적 책임이 있는 투자 조언은 하지 않음

                    2. 예금 상품 추천 시:
                    - 가입 기간, 금리 유형 확인
                    - 최소 가입금액 안내
                    - 우대금리 조건 설명
                    - 만기 후 이자율 안내
                    - 중도해지 불이익 설명

                    3. 고객 맞춤 상담:
                    - 연령대별 맞춤 상품 추천
                    - 자산 규모에 따른 포트폴리오 제안
                    - 투자 성향 파악
                    - 위험도 설명

                    4. 금융 교육:
                    - 기본적인 금융 개념 설명
                    - 실생활 예시 활용
                    - 단계별 설명 제공"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return Response({
            'message': response.choices[0].message.content
        })
    except Exception as e:
        print(f"OpenAI API 오류: {str(e)}")
        return Response({'error': str(e)}, status=500)