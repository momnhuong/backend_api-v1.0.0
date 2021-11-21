import time
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ParseError
from api.models import Account
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from common.jwt import encode_data
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission

from django.core.mail import EmailMessage

@api_view(['GET'])
def user_level(request, *args, **kwargs):

    USER_LV1_VALUE = 'TapSu'
    USER_LV2_VALUE = 'PhuBep'
    USER_LV3_VALUE = 'BepTruong'

    USER_LV1_TEXT = 'Tập sự'
    USER_LV2_TEXT = 'Phụ bếp'
    USER_LV3_TEXT = 'Bếp trưởng'

    LEVELS = [{
      'value': USER_LV1_VALUE,
      'text': USER_LV1_TEXT
    }, {
      'value': USER_LV2_VALUE,
      'text': USER_LV2_TEXT
    }, {
      'value': USER_LV3_VALUE,
      'text': USER_LV3_TEXT
    }]

    return Response(LEVELS, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_level(request, *args, **kwargs):

    LEVEL_DE = 'Dễ'
    LEVEL_TRUNGBINH = 'Trung Bình'
    LEVEL_KHO = 'Khó'

    LEVELS = [{
      'value': 'DE',
      'text': LEVEL_DE
    }, {
      'value': 'TRUNG_BINH',
      'text': LEVEL_TRUNGBINH
    }, {
      'value': 'KHO',
      'text': LEVEL_KHO
    }]

    return Response(LEVELS, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_category(request, *args, **kwargs):
  
    CATEGORIES = (
      ('KHAI_VI', 'Khai vị'),
      ('MON_CHINH', 'Món chính'),
      ('TRANG_MIENG', 'Tráng miệng'),
      ('BANH_NGOT', 'Bánh ngọt'),
      ('AN_CHOI', 'Ăn chơi'),
    )

    CATEGORIES = [{
      'value': 'KHAI_VI',
      'text': 'Khai vị'
    }, {
      'value': 'MON_CHINH',
      'text': 'Món chính'
    }, {
      'value': 'TRANG_MIENG',
      'text': 'Tráng miệng'
    }, {
      'value': 'BANH_NGOT',
      'text': 'Bánh ngọt'
    }, {
      'value': 'AN_CHOI',
      'text': 'Ăn chơi'
    }]

    return Response(CATEGORIES, status=status.HTTP_200_OK)

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()