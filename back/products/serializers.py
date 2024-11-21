# products/serializers.py
from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions, DepositPopularity, SavingPopularity

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'

class DepositPopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositPopularity
        fields = '__all__'

class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    popularity = DepositPopularitySerializer(read_only=True)

    class Meta:
        model = DepositProducts
        fields = '__all__'

class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'

class SavingPopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingPopularity
        fields = '__all__'

class SavingProductsSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    popularity = DepositPopularitySerializer(read_only=True)

    class Meta:
        model = SavingProducts
        fields = '__all__'