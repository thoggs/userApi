from rest_framework.permissions import IsAuthenticated

from userApi import settings

import os
from django.conf import settings
from distutils.util import strtobool


class PermissionSettings:
    def __init__(self, permission_classes=None):
        self.permission_classes = permission_classes or []

    def get_permission_classes(self):
        if 'ENABLE_PERMISSION' in os.environ and os.environ['ENABLE_PERMISSION'] not in ('', None):
            enable_permissions = bool(strtobool(os.environ['ENABLE_PERMISSION']))
        else:
            enable_permissions = getattr(settings, 'ENABLE_PERMISSION', True)
        return self.permission_classes if enable_permissions else []

    def add_permission_class(self, permission_class):
        self.permission_classes.append(permission_class)

    def remove_permission_class(self, permission_class):
        if permission_class in self.permission_classes:
            self.permission_classes.remove(permission_class)

    @staticmethod
    def is_authenticated():
        return IsAuthenticated
