from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import CustomerAccountSerializer, ListCustomerAccountSerializer, EditCustomerAccountSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import SPAAccessPermission

__all__ = ['DetailAccountView', 'ListCustomerAccountView', 'DetailCustomerAccountView',
           'DetailUpdateCustomerAccountView']


class ListCustomerAccountView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: ListCustomerAccountSerializer(many=True),
        },
        tags=['admin/customer/account'],
        operation_id='List Customer Account'
    )
    def get(self, request):
        account = Account.objects.all().filter(
            role__in=Role.objects.all().exclude(name='SUPPER_ADMIN'))
        queryset = self.filter_queryset(account)
        page = self.paginate_queryset(queryset)
        serializer = ListCustomerAccountSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class DetailCustomerAccountView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(

        responses={
            200: CustomerAccountSerializer,
        },
        tags=['admin/customer/account'],
        operation_id='Get Detail Customer Account'
    )
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        try:
            account = Account.objects.all().filter(customer_of=customer_id)
        except:
            payload: dict = {
                'message': 'Customer not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerAccountSerializer(account, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetailUpdateCustomerAccountView(generics.UpdateAPIView, generics.DestroyAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        request_body=EditCustomerAccountSerializer,
        responses={
            200: EditCustomerAccountSerializer,
        },
        tags=['admin/customer/account'],
        operation_id='Edit Customer Account'
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=EditCustomerAccountSerializer,
        responses={
            200: EditCustomerAccountSerializer,
        },
        tags=['admin/customer/account'],
        operation_id='Patch Customer Account'
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        partial = kwargs.pop('partial', False)
        try:
            account = Account.objects.get(id=account_id)
        except:
            payload: dict = {
                'message': 'Account not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        serializer = EditCustomerAccountSerializer(
            account, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['admin/customer/account'],
        operation_id='Delete Customer Account'
    )
    def delete(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        try:
            account = Account.objects.get(id=account_id)
        except:
            payload: dict = {
                'message': 'Account not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        account.set_on_active(False)
        payload: dict = {
            'status': 'success',
            'message': 'Delete success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)


class DetailAccountView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(

        responses={
            200: CustomerAccountSerializer,
        },
        tags=['admin/customer/account'],
        operation_id='Get Detail Account'
    )
    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('account_id')
        try:
            account = Account.objects.get(id=account_id)
        except:
            payload: dict = {
                'message': 'Account not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerAccountSerializer(account, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
