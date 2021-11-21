
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Contract, ProductOfOrder, PackageOfProductOrder, Billing
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import ContractCustomerSerializer, DetailContractCustomerSerializer
from api.supper_admin.billing.serializers import BillingSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from functools import reduce
from backend.pagination import CustomPagination
from django_filters import rest_framework as filters

__all__ = ['ListBillingCustomerView', 'DetailBillingCustomerView']


class ListBillingCustomerFilter(filters.FilterSet):
    class Meta:
        model = Billing
        fields = ('payment_status', 'invoice_number')


class ListBillingCustomerView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    pagination_class = CustomPagination
    filterset_class = ListBillingCustomerFilter

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
        tags=['billing'],
        operation_id='List Billing'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        customer_id = request.user['customer']
        billings = []
        contract = Contract.objects.all().filter(customer_id=customer_id)
        print('contract: ', contract)
        if not contract:
            billings = Billing.objects.filter(id='999999999999999999')
        else:
            billings = Billing.objects.filter(
                reduce(lambda x, y: x | y, [Q(contract=item) for item in contract])).order_by('-created_at')
            # for i in billings:
            #     order_id = i.contract.order_id
            #     product_of_order = ProductOfOrder.objects.all().filter(order_id=order_id)
            #     packages = PackageOfProductOrder.objects.filter(
            #         reduce(lambda x, y: x | y, [Q(product_of_order=item) for item in product_of_order]))
            #     setattr(i.contract, 'service', packages)
        queryset = self.filter_queryset(billings)
        page = self.paginate_queryset(queryset)
        serializer = BillingSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class DetailBillingCustomerView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: BillingSerializer,
        },
        tags=['billing'],
        operation_id='Detail Billing'
    )
    def get(self, request, *args, **kwargs):
        billing_id = kwargs.get('billing_id')
        try:
            billing = Billing.objects.get(
                id=billing_id)
            contract = Contract.objects.get(id=billing.contract_id)
            if request.user['customer'] != contract.customer_id:
                payload: dict = {
                    'message': 'Billing not found',
                    'message_code': '400',
                    'error': {}
                }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        except:
            payload: dict = {
                'message': 'Billing not found',
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
