from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import RegisterSerializer, UserProfileSerializer, AccountSerializer, UserProfileEditSerializer, CreateAccountSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission, AllAccessPermission


class CreateAccountView(generics.CreateAPIView):

    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        request_body=CreateAccountSerializer,
        responses={
            201: CreateAccountSerializer,
        },
        tags=['account'],
        operation_id='Add New Account'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer_class = CreateAccountSerializer(data=request.data)
        if serializer_class.is_valid():
            self.perform_create(serializer_class)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    # @api_view(['POST'])
    # def create_account(request, *args, **kwargs):
    #     username = request.data.get('username', None)
    #     password = request.data.get('password', None)
    #     fullname = request.data.get('fullname', None)
    #     email = request.data.get('email', None)
    #     if not username or not password:
    #         raise ParseError('Username and password can\'t be empty.')
    #     try:
    #         account = Account(username=username, fullname=fullname,
    #                           email=email, password=password)
    #         # account.password = make_password(password)
    #         account.save()
    #     except Exception as ex:
    #         ParseError('Can\'t create account')
    #     return Response({'status': 'Success'}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def register_account(request):
#     if(request.method == 'POST'):
#         serializer = RegisterSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             account = serializer.save()
#             data['response'] = 'successfully registered a new user!'
#             data['email'] = account.email
#             data['username'] = account.username
#         else:
#             data = serializer.errors
#         return Response(data)


class UserProfileView(generics.UpdateAPIView):
    permission_classes = (AllAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: UserProfileSerializer,
        },
        tags=['profile'],
        operation_id='Profile'
    )
    def get(self, request):
        account = Account.objects.get(id=request.user['jit'])
        serializer = UserProfileSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserProfileEditSerializer,
        responses={
            200: UserProfileEditSerializer,
        },
        tags=['profile'],
        operation_id='Put  Profile'
    )
    def put(self, request, *args, **kwargs):
        account = Account.objects.get(id=request.user['jit'])
        serializer = UserProfileEditSerializer(account, data=request.data)
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
        request_body=UserProfileEditSerializer,
        responses={
            200: UserProfileEditSerializer,
        },
        tags=['profile'],
        operation_id='Patch  Profile'
    )
    def patch(self, request, *args, **kwargs):
        account = Account.objects.get(id=request.user['jit'])
        partial = kwargs.pop('partial', False)
        serializer = UserProfileEditSerializer(
            account, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_201_CREATED,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
