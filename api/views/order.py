from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Order, ProductOfOrder, PackageOfProductOrder
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import ProductSerializer, ListProductSerializer
from api.supper_admin.order_of_customer.serializers import ListOrderSerializer, OrderOfCustomerSerializers, CreateOrderSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from functools import reduce
__all__ = ['ListOrderView', 'DetailOrderView', 'CreateOrderView']


class CreateOrderView(generics.CreateAPIView):

    @swagger_auto_schema(

        request_body=CreateOrderSerializer,
        responses={
            200: CreateOrderSerializer,
        },
        tags=['order'],
        operation_id='Add New Order'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOrderView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['order_id']  # field like
    ordering_fields = '__all__'  # order by
    ordering = '-created_at'
    filterset_fields = ['order_id']

    @swagger_auto_schema(
        responses={
            200: ListOrderSerializer(many=True),
        },
        tags=['order'],
        operation_id='List order',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        order = Order.objects.all().filter(
            customer_id=request.user['customer'], on_active=True)
        queryset = self.filter_queryset(order)
        page = self.paginate_queryset(queryset)
        serializer = ListOrderSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class DetailOrderView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: OrderOfCustomerSerializers,
        },
        tags=['order'],
        operation_id='Order Detail'
    )
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        list_order_customer = Order.objects.all().filter(
            customer_id=request.user['customer'], on_active=True)
        order_customer = Order.objects.get(id=order_id, on_active=True)
        if order_customer in list_order_customer:
            try:
                order = Order.objects.get(id=order_id, on_active=True)
            except:
                payload: dict = {
                    'message': 'Order not found',
                    'message_code': '400',
                    'error': {}
                }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

            product_of_order = ProductOfOrder.objects.all().filter(order_id=order_id)
            packages = PackageOfProductOrder.objects.filter(
                reduce(lambda x, y: x | y, [Q(product_of_order=item) for item in product_of_order]))
            setattr(order, 'service', packages)
            serializer = OrderOfCustomerSerializers(
                order, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        payload: dict = {
            'message': 'Order not found',
            'message_code': '400',
            'error': {}
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
