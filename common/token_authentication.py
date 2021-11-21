from rest_framework import authentication
from .jwt import decode_data
from rest_framework.exceptions import AuthenticationFailed


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token:
            try:
                data_payload = decode_data(token)
                # TODO handle logic authentication

                return (data_payload, None)  # (user, none)
            except:
                raise AuthenticationFailed('Token not found!')

        raise AuthenticationFailed('Token not found')
