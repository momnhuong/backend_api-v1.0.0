
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Contract, Order, ProductOfCustomer, ProductOfOrder, static_info, Catelog, Product, Package
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import CreatePackageSerializer, EditPackageSerializer, PackageSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
__all__ = ['ListPackageView', 'EditPackageView', 'UpdateStatusPackageView']


class ListPackageView(generics.ListAPIView, generics.CreateAPIView):

    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'product__name']  # field like
    ordering_fields = '__all__'  # order by
    ordering = '-created_at'
    filterset_fields = ['name', 'product__name']

    @swagger_auto_schema(
        responses={
            200: PackageSerializer(many=True),
        },
        tags=['admin/package'],
        operation_id='List Package',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        package = Package.objects.all()
        queryset = self.filter_queryset(package)
        page = self.paginate_queryset(queryset)
        serializer = PackageSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(

        request_body=CreatePackageSerializer,
        responses={
            200: CreatePackageSerializer,
        },
        tags=['admin/package'],
        operation_id='Add New Package'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreatePackageSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateStatusPackageView(generics.UpdateAPIView):

    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        tags=['admin/package'],
        operation_id='Edit Status Of Package'
    )
    def put(self, request, *args, **kwargs):
        package_id = kwargs.get('package_id')
        try:
            package = Package.objects.get(id=package_id)
        except:
            payload: dict = {
                'message': 'Package not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        if package.on_active is True:
            package.set_on_active(False)
        else:
            package.set_on_active(True)
        payload: dict = {
            'status': 'success',
            'message': 'Update success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)


class EditPackageView(generics.CreateAPIView, generics.UpdateAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        request_body=EditPackageSerializer,
        responses={
            200: EditPackageSerializer,
        },
        tags=['admin/package'],
        operation_id='Edit Package'
    )
    def put(self, request, *args, **kwargs):
        package_id = kwargs.get('package_id')
        try:
            package = Package.objects.get(id=package_id)
        except:
            payload: dict = {
                'message': 'Package not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditPackageSerializer(package, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_201_CREATED,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EditPackageSerializer,
        responses={
            200: EditPackageSerializer,
        },
        tags=['admin/package'],
        operation_id='Patch Package'
    )
    def patch(self, request, *args, **kwargs):
        package_id = kwargs.get('package_id')
        try:
            package = Package.objects.get(id=package_id)
        except:
            payload: dict = {
                'message': 'Package not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        partial = kwargs.pop('partial', False)
        serializer = EditPackageSerializer(
            package, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_201_CREATED,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['admin/package'],
        operation_id='Delete Package'
    )
    def delete(self, request, *args, **kwargs):
        package_id = kwargs.get('package_id')
        try:
            package = Package.objects.get(
                id=package_id)
        except:
            payload: dict = {
                'message': 'Package not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        package.set_on_active(False)
        payload: dict = {
            'status': 'success',
            'message': 'Delete success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)
