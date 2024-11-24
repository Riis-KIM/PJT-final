# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProductSerializer
from django.contrib.auth import get_user_model

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_products(request):
    user = request.user
    serializer = UserProductSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_email(request):
    email = request.data.get('email')
    exists = get_user_model().objects.filter(email=email).exists()
    return Response({'exists': exists})