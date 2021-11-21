from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role, Static
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from api.serializers import StaticSerializer, EditStaticSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission

__all__ = ['StaticInfoView', 'EditStaticInfoView']


class StaticInfoView(generics.ListAPIView):

    @swagger_auto_schema(
        responses={
            200: StaticSerializer,
        },
        tags=['static'],
        operation_id='Static Info',
        operation_summary='API Public'
    )
    def get(self, request):
        static = Static.objects.all().first()
        serializer = StaticSerializer(static)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditStaticInfoView(generics.UpdateAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        request_body=EditStaticSerializer,
        responses={
            200: EditStaticSerializer,
        },
        tags=['static'],
        operation_id='Edit Static Info'
    )
    def put(self, request, *args, **kwargs):
        try:
            static = Static.objects.all().first()
        except:
            payload: dict = {
                'message': 'Static not found',
                'message_code': '400',
                'error': {}
            }
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        serializer = EditStaticSerializer(static, data=request.data)
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
        request_body=EditStaticSerializer,
        responses={
            200: EditStaticSerializer,
        },
        tags=['static'],
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
        serializer = EditStaticSerializer(
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
