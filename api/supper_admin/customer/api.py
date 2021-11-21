from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Service
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import ListCustomerSerializer, EditCustomerSerializer, CustomerSerializer, DeleteCustomerSerializer, CreateCustomerSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
from backend.pagination import CustomPagination
# from django_filters import rest_framework as filters
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import requests
import json
__all__ = ['ListCustomerView', 'DetailCustomerView', 'CreateCustomerView']


# class ListCustomerFilter(filters.FilterSet):
#     customer_name = filters.CharFilter(lookup_expr='icontains')

#     class Meta:
#         model = Customer
#         fields = ('customer_name', 'requester_id')


class ListCustomerView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)
    # pagination_class = CustomPagination
    # queryset = Customer.objects.all()
    # filterset_class = ListCustomerFilter
    # filter_fields = ('customer_name', 'requester_id')
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['customer_name']  # field like
    ordering_fields = '__all__'  # order by
    ordering = '-created_at'
    filterset_fields = ['customer_name']

    @swagger_auto_schema(
        responses={
            200: ListCustomerSerializer(many=True),
        },
        tags=['admin/customer'],
        operation_id='admin'
    )
    def get(self, request):
        # customers = Customer.objects.filter(on_active=True)
        customers = Customer.objects.all()
        queryset = self.filter_queryset(customers)
        page = self.paginate_queryset(queryset)
        serializer = ListCustomerSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)
        # customers = Customer.objects.all().filter(on_active=True)
        # serializer = ListCustomerSerializer(customers, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCustomerView(generics.CreateAPIView):

    @swagger_auto_schema(

        request_body=CreateCustomerSerializer,
        responses={
            200: CreateCustomerSerializer,
        },
        tags=['admin/customer'],
        operation_id='Add New Customer'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateCustomerSerializer(data=request.data)
        customer_name = request.data['customer_name']
        email = request.data['main_email']
        if serializer.is_valid():
            url = "https://usdctechnology.zendesk.com/api/v2/users.json"
            payload = "{\"user\": {\"name\": \"" + \
                customer_name+"\", \"email\": \""+email+"\"}}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer eea15b7525bdb980227bb314d2d11b819e4681040c4b80cb33b36892de65b72b',
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload.encode('utf-8'))
            try:
                value = response.json()['user']['id']
                self.perform_create(serializer)
                new_customer = Customer.objects.get(
                    main_email=email, on_active=True)
                new_customer.set_requester_id(value)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                payload: dict = {
                    'status': 'error',
                    'message': 'Email is already being used by another user in zendesk system',
                    'message_code': '400',
                }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailCustomerView(generics.ListAPIView, generics.UpdateAPIView, generics.DestroyAPIView):

    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: CustomerSerializer,
        },
        tags=['admin/customer'],
        operation_id='admin'
    )
    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        try:
            customers = Customer.objects.get(id=customer_id)
        except:
            payload: dict = {
                'message': 'Customer not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerSerializer(customers)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EditCustomerSerializer,
        responses={
            200: EditCustomerSerializer,
        },
        tags=['admin/customer'],
        operation_id='Edit Customer'
    )
    def put(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        try:
            customers = Customer.objects.get(id=customer_id)
            accounts = Account.objects.all().filter(customer_of_id=customer_id)
        except:
            payload: dict = {
                'message': 'Customer not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditCustomerSerializer(customers, data=request.data)
        if serializer.is_valid():
            if request.data['on_active'] != customers.on_active and request.data['on_active'] is True and accounts:
                for i in accounts:
                    i.set_on_active(True)
            elif request.data['on_active'] != customers.on_active and request.data['on_active'] is False and accounts:
                for i in accounts:
                    i.set_on_active(False)
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_201_CREATED,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EditCustomerSerializer,
        responses={
            200: EditCustomerSerializer,
        },
        tags=['admin/customer'],
        operation_id='Patch  Customer'
    )
    def patch(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        try:
            customers = Customer.objects.get(id=customer_id)
        except:
            payload: dict = {
                'message': 'Customer not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        partial = kwargs.pop('partial', False)
        serializer = EditCustomerSerializer(
            customers, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_201_CREATED,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['admin/customer'],
        operation_id='Delete Customer'
    )
    def delete(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        try:
            customer = Customer.objects.get(id=customer_id)
            account = Account.objects.all().filter(customer_of=customer_id, on_active=True)
            service = Service.objects.all().filter(customer_id=customer_id, on_active=True)
        except:
            payload: dict = {
                'message': 'Customer not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        customer.set_on_active(False)
        for x in range(len(account)):
            account[x].set_on_active(False)
        for x in range(len(service)):
            service[x].set_on_active(False)

        payload: dict = {
            'status': 'success',
            'message': 'Delete success',
            'message_code': '200',
        }
        return Response(payload, status=status.HTTP_200_OK)
