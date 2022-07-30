from django.shortcuts import render
from rest_framework.response import Response
from .models import Product
from rest_framework.views import APIView
from .serializers import ProductSerializer
from django.http import Http404
from rest_framework import status

class ProductListAPI(APIView): #목록 보여줌
    def get(self, request): #리스트 보여줌
        queryset = Product.objects.all()
        print(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self,requset):
        serializer= ProductSerializer(
            data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailAPI(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, requset, pk, format=None):
        product=self.get_object(pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data)

    def delete(self,request,pk,format=None):
        product=self.get_object(pk)
        product.delete()
        return Response(status=statue.HTTP_204_NO_CONTENT)