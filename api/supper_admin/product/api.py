from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Package
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import ListProductSerializer, EditProductSerializer, CreateProductSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission

__all__ = ['DetailUpdateProductView', 'CreateProductView']


class CreateProductView(generics.CreateAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(

        request_body=CreateProductSerializer,
        responses={
            200: CreateProductSerializer,
        },
        tags=['admin/product'],
        operation_id='Add New Product'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUpdateProductView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        request_body=EditProductSerializer,
        responses={
            200: EditProductSerializer,
        },
        tags=['admin/product'],
        operation_id='Edit Product'
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        partial = kwargs.pop('partial', False)
        try:
            product = Product.objects.get(id=product_id)
        except:
            payload: dict = {
                'message': 'Product not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        serializer = EditProductSerializer(
            product, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EditProductSerializer,
        responses={
            200: EditProductSerializer,
        },
        tags=['admin/product'],
        operation_id='Patch Product'
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['admin/product'],
        operation_id='Delete Customer Account'
    )
    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except:
            payload: dict = {
                'message': 'Product not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        product.set_on_active(False)
        for it in Package.objects.all():
            if it.product_id == product_id:
                it.set_on_active(False)
        payload: dict = {
            'status': 'success',
            'message': 'Delete success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)
