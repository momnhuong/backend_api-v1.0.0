from rest_framework import permissions


class TokenPermission(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if request.user:
            # TODO handle logic permission

            return request.user
        else:
            raise PermissionError('Permission denied.')
