import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


def encode_data(data: dict) -> str:
    try:
        payload = jwt.encode(data, settings.JWT_SECRET_KEY, algorithm='HS256')
        return payload
    except jwt.DecodeError as identifier:
        raise exceptions.AuthenticationFailed('Your token is invalid, login!')
    except jwt.ExpiredSignatureError as identifier:
        raise exceptions.AuthenticationFailed('Your token is expired, login!')


def decode_data(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.DecodeError as identifier:
        raise exceptions.AuthenticationFailed('Your token is invalid, login!')
    except jwt.ExpiredSignatureError as identifier:
        raise exceptions.AuthenticationFailed('Your token is expired, login!')
