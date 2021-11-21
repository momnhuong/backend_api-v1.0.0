from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Contract, ProductOfOrder, PackageOfProductOrder, Alert
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.supper_admin.alert.serializers import ListAlertSerializer, EditAlertSerializer
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
__all__ = ['ListAlertCustomerView', 'DetailAlertCustomerView']


class ListAlertFilter(filters.FilterSet):
    class Meta:
        model = Alert
        fields = ('read', 'customer')


class ListAlertCustomerView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
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
        tags=['alert'],
        operation_id='List Alert'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        alerts = Alert.objects.all().filter(
            customer_id=request.user['customer']).order_by('-created_at')
        queryset = self.filter_queryset(alerts)
        page = self.paginate_queryset(queryset)
        serializer = ListAlertSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)


class DetailAlertCustomerView(generics.ListAPIView, generics.UpdateAPIView):
    # permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: ListAlertSerializer,
        },
        tags=['alert'],
        operation_id='Detail Alert'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        alert_id = kwargs.get('alert_id')
        try:
            alerts = Alert.objects.get(id=alert_id)
            print(request.user['role'], alerts.customer_id,
                  request.user['customer'])
            if request.user['role'] != Account.SUPPER_ADMIN and alerts.customer_id != request.user['customer']:
                payload = {
                    'message': 'Alert not found',
                    'message_code': '400',
                    'error': {}
                }
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        except:
            payload = {
                'message': 'Alert not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = ListAlertSerializer(alerts, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EditAlertSerializer,
        responses={
            200: EditAlertSerializer,
        },
        tags=['alert'],
        operation_id='Edit Alert'
    )
    def put(self, request, *args, **kwargs):
        alert_id = kwargs.get('alert_id')
        try:
            alert = Alert.objects.get(id=alert_id)
        except:
            payload: dict = {
                'message': 'Alert not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditAlertSerializer(alert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_200_OK,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=EditAlertSerializer,
        responses={
            200: EditAlertSerializer,
        },
        tags=['alert'],
        operation_id='Patch Package'
    )
    def patch(self, request, *args, **kwargs):
        alert_id = kwargs.get('alert_id')
        try:
            alert = Alert.objects.get(id=alert_id)
        except:
            payload: dict = {
                'message': 'Alert not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        partial = kwargs.pop('partial', False)
        serializer = EditAlertSerializer(
            alert, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_200_OK,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
