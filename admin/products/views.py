from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response 
#from rest_framework.views import APIView
from .models import Product, User
from .producer import publish
from .serializers import ProductSerializer, UserSerializer
import random

# Create your views here.
class ProductViewSet(viewsets.ViewSet):

    def get_list(self, request): 
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def create_product(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("create product request")
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_product(self, request, pk=None):
        products = Product.objects.get(id=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)
    
    def update_product(self, request, pk=None):
        products = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=products, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete_product(self, request, pk=None):
        products = Product.objects.get(id=pk)
        products.delete()
        publish('product_deleted',pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ViewSet):
    
    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_user(self, request, uid=None):
        users = User.objects.get(id=uid)
        serializer = UserSerializer(users)
        return Response(serializer.data)

