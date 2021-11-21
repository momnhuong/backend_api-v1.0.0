from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Static
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import UpdateFcmTokenSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission

__all__ = ['UpdateFcmTokenView']


class UpdateFcmTokenView(generics.UpdateAPIView):
    permission_classes = (CTAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        request_body=UpdateFcmTokenSerializer,
        responses={
            200: UpdateFcmTokenSerializer,
        },
        tags=['fcm_token'],
        operation_id='Update Fcm Token'
    )
    def put(self, request, *args, **kwargs):
        account_id = request.user['jit']
        try:
            account = Account.objects.get(id=account_id)
        except:
            payload: dict = {
                'message': 'Account not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateFcmTokenSerializer(account, data=request.data)
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
        request_body=UpdateFcmTokenSerializer,
        responses={
            200: UpdateFcmTokenSerializer,
        },
        tags=['fcm_token'],
        operation_id='Edit Static Info'
    )
    def patch(self, request, *args, **kwargs):
        try:
            static = Static.objects.all().first()
        except:
            payload: dict = {
                'message': 'Static not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        partial = kwargs.pop('partial', False)
        serializer = UpdateFcmTokenSerializer(
            static, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message_code': status.HTTP_201_CREATED,
                'message': 'Update success',
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
