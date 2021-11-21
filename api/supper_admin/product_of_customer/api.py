from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Order, ProductOfCustomer, Service
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import ProductOCSerializer, ListProductOCSerializer, EditProductOCSerializer, DetailProductOCSerializers, CreateServiceSerializer, CreateProductOfCustomerSerializer, FullProductOfCustomerSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission

__all__ = ['ListProductOfCustomerView',
           'DetailProductOfCustomerView', 'CreateProductOfCustomer', 'UpdateStatusProductOfCustomerView', 'DetailProductOfCustomerItemView']


class CreateProductOfCustomer(generics.CreateAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(

        request_body=CreateProductOfCustomerSerializer,
        responses={
            200: CreateProductOfCustomerSerializer,
        },
        tags=['admin/product_of_customer'],
        operation_id='Add New Product'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateProductOfCustomerSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProductOfCustomerView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: ListProductOCSerializer(many=True),
        },
        tags=['admin/product_of_customer'],
        operation_id='List Product Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        service = Service.objects.all().filter(on_active=True)
        queryset = self.filter_queryset(service)
        page = self.paginate_queryset(queryset)
        serializer = ListProductOCSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)
        # serializer = ListProductOCSerializer(service, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(

        request_body=CreateServiceSerializer,
        responses={
            200: CreateServiceSerializer,
        },
        tags=['admin/product_of_customer'],
        operation_id='Add new Product For Customer'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailProductOfCustomerView(generics.ListAPIView, generics.DestroyAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: ProductOCSerializer,
        },
        tags=['admin/product_of_customer'],
        operation_id='Detail Order Of Customer'
    )
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        items = []
        created_at = []
        try:
            service = Service.objects.get(
                customer_id=customer_id, on_active=True)
        except:
            payload: dict = {
                'message': 'Product not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        products = ProductOfCustomer.objects.all().filter(
            customer_id=customer_id)
        queryset = self.filter_queryset(products)
        page = self.paginate_queryset(queryset)
        serializer = FullProductOfCustomerSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['admin/product_of_customer'],
        operation_id='Delete Order Of Customer'
    )
    def delete(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        try:
            service = Service.objects.get(
                customer_id=customer_id, on_active=True)
        except:
            payload: dict = {
                'message': 'Customer not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        service.set_on_active(False)
        for it in ProductOfCustomer.objects.all():
            if it.customer_id == customer_id:
                it.set_on_active(False)
        payload: dict = {
            'status': 'success',
            'message': 'Delete success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)


class UpdateStatusProductOfCustomerView(generics.UpdateAPIView):

    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        tags=['admin/product_of_customer'],
        operation_id='Edit Status Product Of Cusomter'
    )
    def put(self, request, *args, **kwargs):
        product_of_customer_id = kwargs.get('product_of_customer_id')
        try:
            product_of_customer = ProductOfCustomer.objects.get(
                id=product_of_customer_id)
        except:
            payload: dict = {
                'message': 'Product of Customer not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        if product_of_customer.on_active is True:
            product_of_customer.set_on_active(False)
        else:
            product_of_customer.set_on_active(True)
        payload: dict = {
            'status': 'success',
            'message': 'Update success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)


class DetailProductOfCustomerItemView(generics.ListAPIView, generics.UpdateAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: FullProductOfCustomerSerializer,
        },
        tags=['admin/product_of_customer'],
        operation_id='Detail Item Product Of Customer'
    )
    def get(self, request, *args, **kwargs):
        product_of_customer_id = kwargs.get('product_of_customer_id')
        try:
            product_of_customer = ProductOfCustomer.objects.get(
                id=product_of_customer_id)
        except:
            payload: dict = {
                'message': 'Product not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = FullProductOfCustomerSerializer(
            product_of_customer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EditProductOCSerializer,
        responses={
            200: EditProductOCSerializer,
        },
        tags=['admin/product_of_customer'],
        operation_id='Edit Product Of Customer Detail'
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        product_of_customer_id = kwargs.get('product_of_customer_id')
        partial = kwargs.pop('partial', False)
        try:
            product_of_customer = ProductOfCustomer.objects.get(
                id=product_of_customer_id)
        except:
            payload: dict = {
                'message': 'Product not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditProductOCSerializer(
            product_of_customer, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EditProductOCSerializer,
        responses={
            200: EditProductOCSerializer,
        },
        tags=['admin/product_of_customer'],
        operation_id='Patch Product Of Customer'
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
