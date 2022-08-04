from django.shortcuts import render
from rest_framework.response import Response
from .models import Product
from rest_framework.views import APIView
from .serializers import ProductSerializer
from django.http import Http404
from rest_framework import status, viewsets
#from .inference_code import predict
from .apps import ProductConfig 
import json

class ProductListAPI(viewsets.ViewSet): #목록 보여줌
    serializer_class  = ProductSerializer
    queryset = Product.objects.all()
    
    def get(self, request): #리스트 보여줌
        queryset = Product.objects.all()
        print(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self,requset):
        serializer= ProductSerializer(
            data=requset.data)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    
    
class ProductPredictAPI(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

            
    def get(self, requset, pk, format=None):
        product=self.get_object(pk)
        serializer=ProductSerializer(product)
        
        img_name=serializer.data['image'].split('/')
        image_name=str(img_name[-1])
        predictions=ProductConfig.model.predict(image_name)
        serializer=ProductSerializer(serializer.data,data=predictions,many=True)

        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self,request,pk,format=None):
        product=self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
