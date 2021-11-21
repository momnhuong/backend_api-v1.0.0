from rest_framework import permissions
from .models import Account, Role
from django.conf import settings


class CTAccessPermission(permissions.BasePermission):
    message = 'Permission denied '

    def has_permission(self, request, view):
        _allowed_role = Role.objects.all().exclude(name=Account.SUPPER_ADMIN)
        _equal_role = Role.objects.get(name=request.user['role'])
        if _equal_role in _allowed_role:
            return True
        return False


class SPAAccessPermission(permissions.BasePermission):
    message = 'Permission denied '

    def has_permission(self, request, view):
        _allowed_role = [Role.objects.get(name=Account.SUPPER_ADMIN)]
        _equal_role = Role.objects.get(name=request.user['role'])
        if _equal_role in _allowed_role:
            return True
        return False


class AllAccessPermission(permissions.BasePermission):
    message = 'Permission denied '

    def has_permission(self, request, view):
        _allowed_role = Role.objects.all()
        _equal_role = Role.objects.get(name=request.user['role'])
        if _equal_role in _allowed_role:
            return True
        return False


class PushAlertMessagePermission(permissions.BasePermission):
    message = 'Permission denied'

    def has_permission(self, request, view):
        _allowed_role = 'ALERT'
        if request.user['role'] == _allowed_role:
            return True
        return False
