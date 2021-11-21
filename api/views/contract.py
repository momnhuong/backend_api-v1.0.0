from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Contract, ProductOfOrder, PackageOfProductOrder
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import ContractCustomerSerializer, DetailContractCustomerSerializer
from api.supper_admin.contract.serializers import DetailContractSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from functools import reduce

__all__ = ['ListContractCustomerView', 'DetailContractCustomerView']


class ListContractCustomerView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['contract_id']  # field like
    ordering_fields = '__all__'  # order by
    ordering = '-created_at'
    filterset_fields = ['contract_id']

    @swagger_auto_schema(
        responses={
            200: ContractCustomerSerializer(many=True),
        },
        tags=['contract'],
        operation_id='List Contract'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        contracts = Contract.objects.all().filter(
            customer_id=request.user['customer'], on_active=True).order_by('-created_at')
        serializer = ContractCustomerSerializer(contracts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailContractCustomerView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: DetailContractCustomerSerializer,
        },
        tags=['contract'],
        operation_id='Detail Contract'
    )
    def get(self, request, *args, **kwargs):
        contract_id = kwargs.get('contract_id')
        try:
            contract = Contract.objects.get(
                id=contract_id, on_active=True)
        except:
            payload: dict = {
                'message': 'Contract not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        order_id = contract.order_id
        product_of_order = ProductOfOrder.objects.all().filter(order_id=order_id)
        packages = PackageOfProductOrder.objects.filter(
            reduce(lambda x, y: x | y, [Q(product_of_order=item) for item in product_of_order]))
        setattr(contract, 'service', packages)
        serializer = DetailContractSerializer(contract, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
