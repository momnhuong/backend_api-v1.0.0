from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from api.models import Account, Customer, Role
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .serializers import RoleSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permission import CTAccessPermission, SPAAccessPermission

__all__ = ['ListRoleView']


class ListRoleView(generics.ListAPIView):
    permission_classes = (SPAAccessPermission,)
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        responses={
            200: RoleSerializer(many=True),
        },
        tags=['admin/role'],
        operation_id='List Role'
    )
    def get(self, request):
        role = Role.objects.all().exclude(name=Account.SUPPER_ADMIN)
        serializer = RoleSerializer(role, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
