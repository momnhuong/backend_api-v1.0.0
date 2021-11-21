from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Order, ProductOfCustomer, Service, Catelog
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import ProductOfCatelogSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission

__all__ = ['ProductOfCatelogView']


class ProductOfCatelogView(generics.ListAPIView):
    # permission_classes = (SPAAccessPermission,)
    # authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: ProductOfCatelogSerializer(many=True),
        },
        tags=['admin/product_of_catelog'],
        operation_id='List Product Of Catelog'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        catelog_id = kwargs.get('catelog_id')
        try:
            catelog = Catelog.objects.get(id=catelog_id, on_active=True)
            product = Product.objects.all().filter(catelog_id=catelog_id, on_active=True)
            queryset = self.filter_queryset(product)
            page = self.paginate_queryset(queryset)
            serializer = ProductOfCatelogSerializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            return Response(data, status=status.HTTP_200_OK)
        except:
            payload: dict = {
                'message': 'Catelog not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        # serializer = ListProductOCSerializer(service, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
