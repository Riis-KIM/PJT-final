# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

@api_view(['POST'])
def user_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username=serializer.validated_data['username']
        password=serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'key': token.key,  # 'key'로 반환하는지 확인
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)