
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Contract, Order, ProductOfCustomer, ProductOfOrder, static_info, Catelog, Product, Package, Billing, PackageOfProductOrder
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import BillingSerializer, CreateBillingSerializer, EditBillingSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
from django.db.models import Q
from functools import reduce
from backend.pagination import CustomPagination
from django_filters import rest_framework as filters
from django.db.models import Prefetch
from api.supper_admin.package_of_order.serializers import PackageOfOrderSerializer
__all__ = ['ListBillingView', 'DetailBillingView']


class ListBillingFilter(filters.FilterSet):
    class Meta:
        model = Billing
        fields = ('payment_status', 'invoice_number')


class ListBillingView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = CustomPagination
    filterset_class = ListBillingFilter
    # filter_fields = ('payment_status', 'invoice_number')
    # ordering = ['-created_at']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='payment_status',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={
            200: BillingSerializer(many=True),
        },
        tags=['admin/billing'],
        operation_id='List Billing',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        billing = Billing.objects.all().order_by('-created_at')
        # billing = Billing.objects.select_related(
        #     'contract__order').all()
        # product_of_order = ProductOfOrder.objects.prefetch_related(
        #     Prefetch('order', queryset=billing))
        # service = PackageOfProductOrder.objects.prefetch_related(
        #     Prefetch('product_of_order', queryset=product_of_order))
        # for i in billing:
        #     setattr(i.contract, 'service', service)
        # for i in billing:
        #     order_id = i.contract.order_id
        #     product_of_order = ProductOfOrder.objects.all().filter(order_id=order_id)
        #     packages = PackageOfProductOrder.objects.filter(
        #         reduce(lambda x, y: x | y, [Q(product_of_order=item) for item in product_of_order]))
        #     setattr(i.contract, 'service', packages)

        queryset = self.filter_queryset(billing)
        print(queryset.query)
        page = self.paginate_queryset(queryset)
        serializer = BillingSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(

        request_body=CreateBillingSerializer,
        responses={
            200: CreateBillingSerializer,
        },
        tags=['admin/billing'],
        operation_id='Add New Billing'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateBillingSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            contract = Contract.objects.get(id=request.data['contract_id'])
            print('i: ', contract)
            contract.set_billed(True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailBillingView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: BillingSerializer,
        },
        tags=['admin/billing'],
        operation_id='Detail Billing'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        billing_id = kwargs.get('billing_id')
        try:
            billing = Billing.objects.get(id=billing_id)
        except:
            payload: dict = {
                'message': 'Billing is not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        order_id = billing.contract.order_id
        product_of_order = ProductOfOrder.objects.all().filter(order_id=order_id)
        packages = PackageOfProductOrder.objects.filter(
            reduce(lambda x, y: x | y, [Q(product_of_order=item) for item in product_of_order]))
        setattr(billing.contract, 'service', packages)
        serializer = BillingSerializer(billing, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EditBillingSerializer,
        responses={
            200: EditBillingSerializer,
        },
        tags=['admin/billing'],
        operation_id='Edit Billing'
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        billing_id = kwargs.get('billing_id')
        partial = kwargs.pop('partial', False)
        try:
            billing = Billing.objects.get(id=billing_id)
        except:
            payload: dict = {
                'message': 'Billing not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        serializer = EditBillingSerializer(
            billing, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EditBillingSerializer,
        responses={
            200: EditBillingSerializer,
        },
        tags=['admin/billing'],
        operation_id='Patch Billing'
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
