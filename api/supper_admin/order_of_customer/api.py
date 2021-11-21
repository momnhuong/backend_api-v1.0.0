from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Order, ProductOfOrder, PackageOfProductOrder
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import OrderSerializer, ListOrderSerializer, OrderOfCustomerSerializers, CreateOrderSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from functools import reduce
__all__ = ['ListOrderOfCustomerView',
           'DetailOrderOfCustomerView']


class ListOrderOfCustomerView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['order_id', 'customer__customer_name']  # field like
    ordering_fields = '__all__'  # order by
    ordering = '-created_at'
    filterset_fields = ['order_id', 'customer__customer_name']

    @swagger_auto_schema(
        responses={
            200: ListOrderSerializer(many=True),
        },
        tags=['admin/order_of_customer'],
        operation_id='List Product Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        order = Order.objects.all().filter(on_active=True)

        queryset = self.filter_queryset(order)
        page = self.paginate_queryset(queryset)
        serializer = ListOrderSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class DetailOrderOfCustomerView(generics.ListAPIView, generics.UpdateAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: OrderOfCustomerSerializers,
        },
        tags=['admin/order_of_customer'],
        operation_id='Detail Order Of Customer'
    )
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
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

    @swagger_auto_schema(
        tags=['admin/order_of_customer'],
        operation_id='Delete Order Of Customer'
    )
    def delete(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = Order.objects.get(id=order_id, on_active=True)
        except:
            payload: dict = {
                'message': 'Order not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order.set_on_active(False)
        for it in ProductOfOrder.objects.all():
            if it.order_id == order_id:
                it.set_on_active(False)
        payload: dict = {
            'status': 'success',
            'message': 'Delete success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)


# class GetOrderOfCustomer(generics.ListAPIView):
#     permission_classes = (SPAAccessPermission,)
#     authentication_classes = (TokenAuthentication,)

#     @swagger_auto_schema(
#         responses={
#             200: OrderSerializer(many=True),
#         },
#         tags=['admin/order_of_customer'],
#         operation_id='List Order Of Customer H',
#     )
#     def get(self, request, *args, **kwargs):
#         customer_id = kwargs.get('customer_id')
#         try:
#             order = Order.objects.all().filter(customer_id=customer_id, on_active=True)
#         except:
#             payload: dict = {
#                 'message': 'Order not found',
#                 'message_code': '400',
#                 'error': {}
#             }
#             return Response(payload, status=status.HTTP_400_BAD_REQUEST)
#         serializer = OrderSerializer(order, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
