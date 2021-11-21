from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Order, ProductOfCustomer
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import GetProductOCSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission, AllAccessPermission


class GetProductOfCustomer(generics.ListAPIView):
    permission_classes = (AllAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: GetProductOCSerializer(many=True),
        },
        tags=['product_of_customer'],
        operation_id='List Order Of Customer H',
    )
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        if customer_id == request.user['customer'] or request.user['customer'] == None:
            try:
                product_oc = ProductOfCustomer.objects.all().filter(
                    customer_id=customer_id, on_active=True)
            except:
                payload: dict = {
                    'message': 'Product not found',
                    'message_code': '400',
                    'error': {}
                }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
            serializer = GetProductOCSerializer(product_oc, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        payload: dict = {
            'message': 'customer_id is not valid',
            'message_code': '400',
            'error': {}
        }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
