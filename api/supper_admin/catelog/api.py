from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Contract, Order, ProductOfCustomer, ProductOfOrder, static_info, Catelog, Product, Package
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import CatelogSerializer, CreateCatelogSerializer, EditCatelogSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission

__all__ = ['ListCatelogView', 'DetailCatelogView']


class ListCatelogView(generics.ListAPIView, generics.CreateAPIView):
    # permission_classes = (SPAAccessPermission,)
    # authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: CatelogSerializer(many=True),
        },
        tags=['admin/catelog'],
        operation_id='List Catelog',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        catelogs = Catelog.objects.all()
        queryset = self.filter_queryset(catelogs)
        page = self.paginate_queryset(queryset)
        serializer = CatelogSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)
        # serializer = ListContractSerializer(contracts, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(

        request_body=CreateCatelogSerializer,
        responses={
            200: CreateCatelogSerializer,
        },
        tags=['admin/catelog'],
        operation_id='Add New Catelog'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateCatelogSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailCatelogView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: CatelogSerializer,
        },
        tags=['admin/catelog'],
        operation_id='Detail Catelog'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        catelog_id = kwargs.get('catelog_id')
        try:
            catelog = Catelog.objects.get(id=catelog_id)
        except:
            payload: dict = {
                'message': 'Catelog is not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = CatelogSerializer(catelog, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EditCatelogSerializer,
        responses={
            200: EditCatelogSerializer,
        },
        tags=['admin/catelog'],
        operation_id='Edit Catelog'
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        catelog_id = kwargs.get('catelog_id')
        partial = kwargs.pop('partial', False)
        try:
            catelog = Catelog.objects.get(id=catelog_id)
        except:
            payload: dict = {
                'message': 'Catelog not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        serializer = EditCatelogSerializer(
            catelog, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EditCatelogSerializer,
        responses={
            200: EditCatelogSerializer,
        },
        tags=['admin/catelog'],
        operation_id='Patch Catelog'
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['admin/catelog'],
        operation_id='Delete Catelog'
    )
    def delete(self, request, *args, **kwargs):
        catelog_id = kwargs.get('catelog_id')
        try:
            catelog = Catelog.objects.get(id=catelog_id)
        except:
            payload: dict = {
                'message': 'Catelog is not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        catelog.set_on_active(False)
        for it in Product.objects.all():
            if it.catelog_id_id == catelog_id:
                it.set_on_active(False)
                for k in Package.objects.all():
                    k.product_id == it.id
                    k.set_on_active(False)

        payload: dict = {
            'status': 'success',
            'message': 'Delete success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)
