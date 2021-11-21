
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Order, ProductOfCustomer, Service, PackageOfProductCustomer, Package, Contract, Billing
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import HomePageListPackageOfSerializer, HomePageListPackageOfNoCustomerSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission
import requests
from django.utils.timezone import now
from decimal import *
__all__ = ['HomePageListPackageOfCustomerSAView',
           'HomePageCountPackageSAView', 'HomePageListTicketSAView', 'HomePageListCustomerOfProductSAView', 'HomePageListBalanceOfCustomerSAView']


class HomePageListPackageOfCustomerSAView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200:  HomePageListPackageOfSerializer(many=True),
        },
        tags=['admin/homepage'],
        operation_id='List Package Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        # package_of_customer = PackageOfProductCustomer.objects.all().filter(on_active=True)
        package_of_customer = ProductOfCustomer.objects.all().filter(on_active=True)
        queryset = self.filter_queryset(package_of_customer)
        page = self.paginate_queryset(queryset)
        serializer = HomePageListPackageOfSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)
        # serializer = ListProductOCSerializer(service, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class HomePageCountPackageSAView(generics.ListAPIView):

    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        # responses={
        #     200:  HomePageListPackageOfSerializer(many=True),
        # },
        tags=['admin/homepage'],
        operation_id='Count Package Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        package_of_customer = PackageOfProductCustomer.objects.all().filter(on_active=True)
        product_of_customer = ProductOfCustomer.objects.all().filter(on_active=True)
        # count
        # arr: product_of_customer
        # 1: return array: [id,id,id,id] (id of package)
        # 2: sort array
        # 3: count each item in array
        arr = []
        data = []
        for i in product_of_customer:
            # arr.append(i.package.id)
            arr.append(Product.objects.get(
                id=i.product.id).id)

        arr.sort()
        k = 1
        for i in range(len(arr)):
            if len(arr) - 1 == i:
                data.append(
                    {'name': Product.objects.get(id=arr[i]).name, 'product_id': Product.objects.get(id=arr[i]).id, 'count': k})
            elif arr[i] != arr[i + 1]:
                data.append({'name': Product.objects.get(
                    id=arr[i]).name, 'product_id': Product.objects.get(id=arr[i]).id, 'count': k})
                k = 1
            else:
                k += 1

        return Response(data, status=status.HTTP_200_OK)


class HomePageListTicketSAView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        # responses={
        #     200:  HomePageListPackageOfSerializer(many=True),
        # },
        tags=['admin/homepage'],
        operation_id='Count Ticket Of Customer'
    )
    def get(self, request, *args, **kwargs):
        url = "https://usdctechnology.zendesk.com/api/v2/search.json?query=type:ticket status:open"
        payload = {}
        headers = {
            'Authorization': 'Basic amFtZXMuY2hlbkB1c2RjLnZuOjEyMzQ1dXNkY0A='
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        data = {}
        try:
            response.json()['count']
            data = dict = {
                'count': response.json()['count'],
            }
        except:
            data = dict = {
                'count': 0,
                'error': 'Fail to fetch Zendesk'
            }
        return Response(data, status=status.HTTP_200_OK)


class HomePageListCustomerOfProductSAView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200:  HomePageListPackageOfSerializer(many=True),
        },
        tags=['admin/homepage'],
        operation_id='List Package Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        product_id = kwargs.get('product_id')
        # package_of_customer = PackageOfProductCustomer.objects.all().filter(on_active=True)
        product_of_customer = ProductOfCustomer.objects.all().filter(
            product_id=product_id, on_active=True)
        arr = []
        data = []
        for i in product_of_customer:
            arr.append(i.customer.id)
        arr.sort()
        for i in range(len(arr)):
            if len(arr) == 1:
                data.append(arr[i])
                # break
            if len(arr) - 1 == i:
                data.append(arr[i])
            elif(arr[i] != arr[i+1]):
                data.append(arr[i])
        new_data = []
        for i in range(len(data)):
            if len(data) - 1 == i:
                service = ProductOfCustomer.objects.all().filter(
                    customer_id=Customer.objects.get(id=data[i]).id, product_id=product_id, on_active=True)
                serializer = HomePageListPackageOfNoCustomerSerializer(
                    service, many=True)
                new_data.append(
                    {'name': Customer.objects.get(id=data[i]).customer_name, 'service': serializer.data, 'tax_code': Customer.objects.get(id=data[i]).tax_code, 'main_email': Customer.objects.get(id=data[i]).main_email, 'phone_number': Customer.objects.get(id=data[i]).phone_number, 'address': Customer.objects.get(id=data[i]).address})
            elif data[i] != data[i + 1]:
                service = ProductOfCustomer.objects.all().filter(
                    customer_id=Customer.objects.get(id=data[i]).id, product_id=product_id, on_active=True)
                serializer = HomePageListPackageOfNoCustomerSerializer(
                    service, many=True)
                new_data.append({'name': Customer.objects.get(id=data[i]).customer_name, 'service': serializer.data, 'tax_code': Customer.objects.get(id=data[i]).tax_code, 'main_email': Customer.objects.get(
                    id=data[i]).main_email, 'phone_number': Customer.objects.get(id=data[i]).phone_number, 'address': Customer.objects.get(id=data[i]).address})

        return Response(new_data, status=status.HTTP_200_OK)
        # serializer = ListProductOCSerializer(service, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class HomePageListBalanceOfCustomerSAView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200:  HomePageListPackageOfSerializer(many=True),
        },
        tags=['admin/homepage'],
        operation_id='List Balance Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, reuqest, *args, **kwargs):
        billings = Billing.objects.all().filter(payment_status=False)
        data = []
        total = 0
        for i in billings:
            contract = Contract.objects.get(id=i.contract_id)
            order = Order.objects.get(id=contract.order_id)
            date = now() - contract.created_at
            expired_day = contract.end_time - now()
            if expired_day.days > 0:
                vat = order.amount * Decimal('0.1')
                data.append({'contract_id': contract.id,
                             'balance': order.amount + vat})
        for i in data:
            total += i['balance']
        result = {
            'total': total,
            'list_detail': data
        }
        return Response(result, status=status.HTTP_200_OK)
