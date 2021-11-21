from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Contract, ProductOfOrder
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import DetailCustomerSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission

__all__ = ['DetailCustomerView']


class DetailCustomerView(generics.ListAPIView):

    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: DetailCustomerSerializer,
        },
        tags=['customer'],
        operation_id='Customer Infos'
    )
    def get(self, request):
        try:
            customer = Customer.objects.get(
                id=request.user['customer'], on_active=True)
        except:
            payload: dict = {
                'message': 'Customer not found',
                'message_code': '400',
                'error': ''
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = DetailCustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
