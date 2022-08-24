from django.shortcuts import render
from rest_framework.response import Response
#-*-coding:utf-8-*-
from .models import Product
from rest_framework.views import APIView
from .serializers import ProductSerializer
from django.http import Http404
from rest_framework import status, viewsets
#from .inference_code import predict
from .apps import ProductConfig 
from itertools import chain
import pandas as pd
import json

class ProductListAPI(viewsets.ModelViewSet): #목록 보여줌
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
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
                

        predictions.update(serializer.data)
        
        json_list=[predictions]
        return Response(json_list, status=status.HTTP_201_CREATED)

    def delete(self,request,pk,format=None):
        product=self.get_object(pk)
        product.delete()
        return Response(status=statue.HTTP_204_NO_CONTENT)