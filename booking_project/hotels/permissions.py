from django.contrib.auth.models import Group
from rest_framework import permissions


class AllForAdminOtherReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            admin_group = Group.objects.get(name='Admin')
            if admin_group in request.user.groups.all():
                return True
        except Group.DoesNotExist:
            pass

        return request.method in permissions.SAFE_METHODS
