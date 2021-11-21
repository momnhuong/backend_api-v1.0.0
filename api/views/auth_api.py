import time
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.exceptions import ParseError
from api.models import Account, Customer
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status, generics
from common.jwt import encode_data, decode_data
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, ChangePasswordSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
# from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import json
import requests


@swagger_auto_schema(
    method='POST',
    request_body=LoginSerializer,
    responses={
        200: LoginSerializer,
    },
    operation_id='Login'
)
@api_view(['POST'])
def login(request):
    # zendesk
    url = "https://usdctechnology.zendesk.com/api/v2/oauth/tokens.json"
    payload = "{\"token\": {\"client_id\": 900000037863, \"scopes\": [\"read\", \"write\"]}}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic amFtZXMuY2hlbkB1c2RjLnZuOjEyMzQ1dXNkY0A='
    }
    # v_cloud
    url_cloud = "https://vpc.vcpp.vn/api/sessions"

    payload_cloud = {}
    headers_cloud = {
        'Accept': 'application/*+json;version=33.0',
        'Authorization': 'Basic dnBjdXNkY3ZpQHVzZGM6QWJjQDEyMzQ1Ng=='
    }

    # response_cloud = requests.request(
    #     "POST", url_cloud, headers=headers_cloud, data=payload_cloud)
    login_serializers = LoginSerializer
    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            bold_fail: dict = {
                'message_code': '1001',
                'error': {}
            }
            return Response(bold_fail, status=status.HTTP_400_BAD_REQUEST)

        account: Account = None
        try:
            account = Account.objects.get(username=username, on_active=True)
        except:
            user_fail: dict = {
                'message': 'Account not found',
                'message_code': '1002',
                'error': {}
            }
            return Response(user_fail, status=status.HTTP_400_BAD_REQUEST)

        if password != account.password:
            pass_fail: dict = {
                'message': 'Password is wrong',
                'message_code': '1003',
                'error': {}
            }
            return Response(pass_fail, status=status.HTTP_400_BAD_REQUEST)

        EXPIRY_TIME = int(time.time()) + settings.TOKEN_EXPIRATION_DURATION
        CURRENT_TIME = int(time.time())

        account.set_last_login()
        if account.role.name == Account.SUPPER_ADMIN:
            customer = None
        else:
            customer = Customer.objects.get(id=account.customer_of_id)
            customer = customer.requester_id

        response_zendesk = requests.request(
            "POST", url, headers=headers, data=payload)
        zendesk = {}
        v_cloud = {}
        # zendesk
        try:
            response_zendesk.json()['token']
            zendesk = dict = {
                'token': {
                    'full_token': response_zendesk.json()['token']['full_token']
                },
            }
        except:
            zendesk = dict = {
                'token': {'full_token': '',
                          'error': 'Fail to fetch Zendesk'}
            }

        # v_cloud

        data_payload = {
            'jit':  str(account.pk),
            'role': account.role.name,
            'customer': account.customer_of_id,
            'requester_id': customer,
            'exp': EXPIRY_TIME,
            'iat':  CURRENT_TIME
        }
        token = encode_data(data_payload)
        data_response: dict = {
            'id': str(account.pk),
            'fullname': account.fullname,
            'customer': account.customer_of_id,
            'role': account.role.name,
            'first_login': account.first_login,
            'requester_id': customer,
            'exp': EXPIRY_TIME,
            'iat': CURRENT_TIME,
            'token': token,
            'fcm_token': account.fcm_token,
            'zendesk': zendesk,
            'v_cloud': v_cloud,
        }
        return Response(data_response, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='POST',
    request_body=LogoutSerializer,
    responses={
        200: LogoutSerializer,
    },
    operation_id='Logout'
)
@api_view(['POST'])
def logout(request):
    logout_serializers = LogoutSerializer
    url_logout = "https://usdctechnology.zendesk.com/api/v2/oauth/tokens/" + \
        request.data.get('zendesk_id', None) + ".json"

    payload = {}
    headers = {
        'Authorization': 'Basic Y3Vvbmdsc0B1c2RjLnZuOjEyMzQ1dXNkY0A=',
        'Cookie': '__cfduid=d20d1a835cabe8587f18485732ff8210e1600165733; __cfduid=d684e3d5bf9003e425777ab289d48a02e1600173561; __cfruid=1ebfcef2b234cb591c0476580ca81f558e08237a-1600659615'
    }
    response = requests.request(
        "DELETE", url_logout, headers=headers, data=payload)

# @api_view(['POST'])
# @authentication_classes((TokenAuthentication, ))
# @permission_classes((TokenPermission, ))
# def check_jwt_token(request, *args, **kwargs):
#     user_data = request.user
#     return Response(user_data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @authentication_classes((TokenAuthentication, ))
# @permission_classes((TokenPermission, ))
# def refresh_token(request, *args, **kwargs):
#     user_data = request.user

#     EXPIRY_TIME = int(time.time()) + settings.TOKEN_EXPIRATION_DURATION
#     CURRENT_TIME = int(time.time())

#     data_payload: dict = {
#         'jit': user_data["jit"],
#         'level': 'ADMIN',
#         'exp': EXPIRY_TIME,
#         'iat':  CURRENT_TIME
#     }

#     token = encode_data(data_payload)
#     date_response: dict = {
#         'token': token,
#         'exp': EXPIRY_TIME,
#         'iat': CURRENT_TIME
#     }

#     return Response(date_response, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    # permission_classes = (TokenPermission,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.data.get('new_password')
            if Account.objects.get(id=self.object['jit']).password == serializer.data.get('old_password'):
                Account.objects.get(
                    id=self.object['jit']).set_new_password(new_password)
                response = {
                    'status': 'success',
                    'message_code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                data_payload: dict = {
                    'status': 'failed',
                    'message': 'Old password is invalid',
                    'message_code': status.HTTP_400_BAD_REQUEST,
                    'error': {}
                }
                return Response(data_payload, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            if Account.objects.filter(email=email).exists():
                user = Account.objects.get(email=email)
                user.set_last_login()
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                absurl = settings.HOST_RESET_PASSWORD
                email_body = 'Hello ' + user.fullname + '\nUse link below to reset your password  \n' + \
                    absurl + "/?token=" + token + '&uidb64=' + uidb64
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reset your passsword'}
                Util.send_email(data)
                data_payload: dict = {
                    'status': 'success',
                    'message': 'We have sent you a link to reset your password',
                    'message_code': status.HTTP_200_OK,
                    'error': {}
                }
                return Response(data_payload, status=status.HTTP_200_OK)
            else:
                data_payload: dict = {
                    'status': 'error',
                    'message': 'Email not found, please check email again!',
                    'message_code': status.HTTP_400_BAD_REQUEST,
                    'error': {}
                }
                return Response(data_payload, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordResetEmail(generics.GenericAPIView):

    serializer_class = SetNewPasswordSerializer

    def patch(self, request, *args, **kwargs):
        try:
            id = smart_str(urlsafe_base64_decode(request.data['uidb64']))
            token = request.data['token']
            if Account.objects.filter(id=id).exists() is False:
                data_payload: dict = {
                    'status': 'error',
                    'message': 'Uidb64 is not valid',
                    'message_code': status.HTTP_401_UNAUTHORIZED,
                    'error': {}
                }
                return Response(data_payload, status=status.HTTP_401_UNAUTHORIZED)
            else:
                user = Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                data_payload: dict = {
                    'status': 'error',
                    'message': 'Token is not valid, please request a new one!',
                    'message_code': status.HTTP_401_UNAUTHORIZED,
                    'error': {}
                }
                return Response(data_payload, status=status.HTTP_401_UNAUTHORIZED)

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_new_password(request.data['password'])
            user.set_last_login()
            data_payload: dict = {
                'status': 'success',
                'message': 'Password reset success',
                'message_code': status.HTTP_200_OK,
                'error': {}
            }
            return Response(data_payload, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                data_payload: dict = {
                    'status': 'error',
                    'message': 'Token is not valid, please request a new one!',
                    'message_code': status.HTTP_401_UNAUTHORIZED,
                    'error': {}
                }
                return Response(data_payload, status=status.HTTP_401_UNAUTHORIZED)
