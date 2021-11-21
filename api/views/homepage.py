from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Product, Order, ProductOfCustomer, PackageOfProductCustomer, Package, Contract, Catelog, Alert
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import GetProductOCSerializer, HomePageGetProductOCSerializer, HomePageGetAllProductOCSerializer
from api.serializers.product import ProductSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission, AllAccessPermission
import requests
from django.utils.timezone import now
from django.db.models import Q
from functools import reduce
from decimal import *
from django.db.models import Prefetch
__all__ = ['HomePageListPackageOfCustomerCView',
           'HomePageCountPackageOfCustomerCView', 'HomePageListTicketCView', 'HomePageListCustomerOfProductSAView', 'HomePageListBalanceOfCustomerCTView',
           'HomePageCountAlertCTView']


class HomePageListPackageOfCustomerCView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200:  HomePageGetProductOCSerializer(many=True),
        },
        tags=['homepage'],
        operation_id='List Package Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        customer_id = request.user['customer']
        product_of_customer = ProductOfCustomer.objects.filter(
            customer_id=customer_id, on_active=True)
        catelogs = []
        result = []
        keep = 0
        for i in product_of_customer:
            catelogs.append({'product_of_customer': i, 'catelog': Catelog.objects.get(
                id=Product.objects.get(id=i.product_id).catelog_id_id).id})
        for i in catelogs:
            if not result:
                print('ne ne: ', i['catelog'])
                result.append({'catelog': i['catelog'], 'product_of_customer': [
                               i['product_of_customer']]})
            else:
                keep = 0
                for k in result:
                    if k['catelog'] == i['catelog']:
                        keep += 1
                        k['product_of_customer'].append(
                            i['product_of_customer'])
                if keep == 0:
                    result.append({'catelog': i['catelog'], 'product_of_customer': [
                        i['product_of_customer']]})
        for i in result:
            i['catelog'] = Catelog.objects.get(id=i['catelog'])
        queryset = self.filter_queryset(result)
        page = self.paginate_queryset(queryset)
        serializer = HomePageGetProductOCSerializer(page, many=True)
        data = self.get_paginated_response(serializer.data).data
        # result = self.get_paginated_response(serializer.data)
        # data = result.data
        # serializer = ProductSerializer(product_of_customer, many=True)
        return Response(data, status=status.HTTP_200_OK)


class HomePageCountPackageOfCustomerCView(generics.ListAPIView):

    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        # responses={
        #     200:  HomePageGetProductOCSerializer(many=True),
        # },
        tags=['homepage'],
        operation_id='Count Package Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        customer_id = request.user['customer']
        product_of_customer = ProductOfCustomer.objects.all().filter(
            customer_id=customer_id, on_active=True)
        # list_package = PackageOfProductCustomer.objects.all().filter(on_active=True)
        # for item_i in product_of_customer:
        #     setattr(item_i, 'package_of_customer', [])
        #     for item_k in list_package:
        #         if item_k.product_of_customer_id == item_i.id:
        #             item_i.package_of_customer.append(item_k)

        # count
        # arr: product_of_customer
        # 1: return array: [id,id,id,id] (id of package)
        # 2: sort array
        # 3: count each item in array

        # todo
        # arr = []
        # data = []
        # for i in product_of_customer:
        #     for k in i.package_of_customer:
        #         # arr.append(k.package.id)
        #         arr.append(Product.objects.get(
        #             id=Package.objects.get(id=k.package.id).product_id).id)

        # arr.sort()
        # k = 1
        # for i in range(len(arr)):
        #     if len(arr) - 1 == i:
        #         data.append(
        #             {'name': Product.objects.get(id=arr[i]).name, 'count': k})
        #     elif arr[i] != arr[i + 1]:
        #         data.append({'name': Product.objects.get(
        #             id=arr[i]).name, 'count': k})
        #         k = 1
        #     else:
        #         k += 1

        # return Response(data, status=status.HTTP_200_OK)

        arr = []
        data = []
        for i in product_of_customer:
            arr.append(i.product.id)

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


class HomePageListTicketCView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        # responses={
        #     200:  HomePageGetProductOCSerializer(many=True),
        # },
        tags=['homepage'],
        operation_id='Count Ticket Of Customer'
    )
    def get(self, request, *args, **kwargs):
        url = "https://usdctechnology.zendesk.com/api/v2/search.json?query=type:ticket status:open requester_id:" + \
            request.user['requester_id']
        payload = 'query=type%3Aticket%20requester_id%3A' + \
            request.user['requester_id']
        headers = {
            'Authorization': 'Basic amFtZXMuY2hlbkB1c2RjLnZuOjEyMzQ1dXNkY0A=',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return Response({'count': response.json()['count']}, status=status.HTTP_200_OK)


class HomePageListCustomerOfProductSAView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200:  HomePageGetProductOCSerializer(many=True),
        },
        tags=['homepage'],
        operation_id='List Package Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        customer_id = request.user['customer']
        # package_of_customer = PackageOfProductCustomer.objects.all().filter(on_active=True)
        product_of_customer = ProductOfCustomer.objects.all().filter(
            product_id=product_id, customer_id=customer_id, on_active=True)
        queryset = self.filter_queryset(product_of_customer)
        page = self.paginate_queryset(queryset)
        serializer = HomePageGetAllProductOCSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)
        data = result.data
        return Response(data, status=status.HTTP_200_OK)
        # serializer = ListProductOCSerializer(service, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class HomePageListBalanceOfCustomerCTView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        # responses={
        #     200:  HomePageListPackageOfSerializer(many=True),
        # },
        tags=['homepage'],
        operation_id='Balance Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        customer_id = request.user['customer']
        list_contract = Contract.objects.all().filter(customer_id=customer_id)
        list_order = []
        data = []
        total = 0
        for i in list_contract:
            list_order.append(Order.objects.get(id=i.order_id))
        for i in list_order:
            contract = Contract.objects.get(order_id=i.id)
            date = now() - contract.created_at
            vat = i.amount * Decimal('0.1')
            price_vat = i.amount + vat
            expired_day = contract.end_time - now()
            # if date.days > 0 and date.days != i.order_time * 30:
            if expired_day.days > 0:
                data.append({'contract_id': contract.id, 'balance': round(Decimal(
                    price_vat) - ((Decimal(price_vat)/Decimal(i.order_time * 30))*date.days), 2)})
            # elif date.days == 0:
            #     data.append({'contract_id': contract.id, 'balance': round(Decimal(
            #         price_vat))})
            else:
                data.append({'contract_id': contract.id, 'balance': 0})
        for i in data:
            total += i['balance']
        result = {
            'total': total,
            'list_detail': data
        }
        return Response(result, status=status.HTTP_200_OK)


class HomePageCountAlertCTView(generics.ListAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        # responses={
        #     200:  HomePageListPackageOfSerializer(many=True),
        # },
        tags=['homepage'],
        operation_id='Alert Of Customer'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        customer_id = request.user['customer']
        alert = Alert.objects.all().filter(customer_id=customer_id, read=False)
        length = alert.count()
        return Response(length, status=status.HTTP_200_OK)
