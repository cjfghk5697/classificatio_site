#product/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer) :
    image = serializers.ImageField(use_url=True)
    predict= serializers.CharField(max_length=70)
    class Meta :
        model = Product        # product 모델 사용
        fields = ('id','image','predict')           # 모든 필드 포함
    
