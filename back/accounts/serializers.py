# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from products.serializers import DepositProductsSerializer, SavingProductsSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(required=False)
    age = serializers.IntegerField(required=False)
    money = serializers.IntegerField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'name': self.validated_data.get('name', ''),
            'age': self.validated_data.get('age', 0),
            'money': self.validated_data.get('money', None),
        })
        return data

class UserDetailSerializer(serializers.ModelSerializer):
    liked_deposits = DepositProductsSerializer(many=True, read_only=True)
    liked_savings = SavingProductsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'age', 'money', 
                 'liked_deposits', 'liked_savings')
        read_only_fields = ('id', 'liked_deposits', 'liked_savings')