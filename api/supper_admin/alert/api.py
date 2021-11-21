from functools import reduce
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from api.permission import CTAccessPermission, SPAAccessPermission, PushAlertMessagePermission
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from common.token_permission import TokenPermission
from common.token_authentication import TokenAuthentication
from .serializers import ListAlertSerializer, CreateAlertSerializer
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from api.models import Contract, Order, ProductOfCustomer, ProductOfOrder, static_info, PackageOfProductOrder, Alert, Account
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from backend.pagination import CustomPagination
from django_filters import rest_framework as filters
import requests
import json
__all__ = ['ListAlertView', 'CreateAlertView']


class ListAlertFilter(filters.FilterSet):
    class Meta:
        model = Alert
        fields = ('read', 'customer')


class ListAlertView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    pagination_class = CustomPagination
    filterset_class = ListAlertFilter
    filter_fields = ('read', 'customer')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='read',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={
            200: ListAlertSerializer(many=True),
        },
        tags=['admin/alert'],
        operation_id='List Alert'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        alerts = Alert.objects.all().order_by('-created_at')
        queryset = self.filter_queryset(alerts)
        page = self.paginate_queryset(queryset)
        serializer = ListAlertSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class CreateAlertView(generics.CreateAPIView):
    permission_classes = (PushAlertMessagePermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(

        request_body=CreateAlertSerializer,
        responses={
            200: CreateAlertSerializer,
        },
        tags=['admin/alert'],
        operation_id='Add New Alert'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = CreateAlertSerializer(data=request.data)

        if serializer.is_valid():
            product_of_customer = ProductOfCustomer.objects.get(
                system_id=request.data['system_id'])
            accounts = Account.objects.all().filter(
                customer_of_id=product_of_customer.customer_id)
            registration_ids = []
            for i in accounts:
                registration_ids.append(i.fcm_token)
            body_dict = {
                "notification": {
                    "title": "Update Alert Message",
                    "body": "One alert need update"
                },
                "registration_ids": registration_ids
            }
            url = "https://fcm.googleapis.com/fcm/send"
            payload = json.dumps(body_dict)
            headers = {
                'Authorization': 'key=AAAAxcrKjNg:APA91bH778IOlFwCHWskrJpyTArJ2E9-M8d4OefwqbbNkLc0_jmbRulrsMBpt79biEom60QoZGONOczqUcLVX5deANUxaZw4PYlTxp0Qjd1qjE6dHlQ-k6uqEHvYaPhgauaYs1mwGh9B',
                'Content-Type': 'application/json'
            }

            # print(response.text.encode('utf8'))
            try:
                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                # value = response.json()['success']
                # if value > 0:
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                payload: dict = {
                    'status': 'Error Firebase',
                    'message': response.text.encode('utf8'),
                    'message_code': '400',
                }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
