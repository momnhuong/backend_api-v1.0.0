from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import ProductSerializer, ListProductSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission, AllAccessPermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
__all__ = ['ListProductView', 'DetailProductView']


class ListProductView(generics.ListAPIView):
    permission_classes = (AllAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']  # field like
    ordering_fields = '__all__'  # order by
    ordering = '-created_at'
    filterset_fields = ['name']

    @swagger_auto_schema(
        responses={
            200: ListProductSerializer(many=True),
        },
        tags=['product'],
        operation_id='List Product',
        operation_summary="API Public"
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.user['role'] == Account.SUPPER_ADMIN:
            product = Product.objects.all()
        else:
            product = Product.objects.all().filter(on_active=True)
        queryset = self.filter_queryset(product)
        page = self.paginate_queryset(queryset)
        serializer = ListProductSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class DetailProductView(generics.ListAPIView):

    @swagger_auto_schema(
        responses={
            200: ProductSerializer,
        },
        tags=['product'],
        operation_id='Detail Product',
        operation_summary="API Public"
    )
    def get(self, request, *args, **kwargs):
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
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
