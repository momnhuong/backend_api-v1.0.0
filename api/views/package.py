
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Package, Product
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import ContractCustomerSerializer, DetailContractCustomerSerializer
from api.supper_admin.package.serializers import PackageSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission, AllAccessPermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
__all__ = ['ListPackageView',
           'DetailPackageOfProductView', 'DetailPackageView']


class ListPackageView(generics.ListAPIView):
    permission_classes = (AllAccessPermission,)
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
        tags=['package'],
        operation_id='List Package',
        operation_summary='API Public'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.user['role'] == Account.SUPPER_ADMIN:
            package = Package.objects.all()
        else:
            package = Package.objects.all().filter(on_active=True)

        queryset = self.filter_queryset(package)
        page = self.paginate_queryset(queryset)
        serializer = PackageSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class DetailPackageOfProductView(generics.ListAPIView):
    permission_classes = (AllAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: PackageSerializer(many=True),
        },
        tags=['package'],
        operation_id='List Package',
        operation_summary='API Public'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            try:
                if request.user['role'] == Account.SUPPER_ADMIN:
                    package = Package.objects.all().filter(
                        product_id=product_id)
                else:
                    package = Package.objects.all().filter(
                        product_id=product_id, on_active=True)

                serializer = PackageSerializer(package, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                payload: dict = {
                    'message': 'Package not found',
                    'message_code': '400',
                    'error': {}
                }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        except:
            payload: dict = {
                'message': 'Product not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


class DetailPackageView(generics.ListAPIView):
    @swagger_auto_schema(
        responses={
            200: PackageSerializer,
        },
        tags=['package'],
        operation_id='List Package',
        operation_summary='API Public'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        package_id = kwargs.get('package_id')
        try:
            package = Package.objects.get(id=package_id)
            serializer = PackageSerializer(package, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            payload: dict = {
                'message': 'Package not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
