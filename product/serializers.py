#product/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer) :
    image = serializers.ImageField(use_url=True)
    class Meta :
        model = Product        # product 모델 사용
        fields = ('id','predict','image')           # 모든 필드 포함
        

        