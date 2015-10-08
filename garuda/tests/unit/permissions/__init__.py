# -*- coding:utf-8 -*-

from uuid import uuid4

from garuda.plugins.default_permissions_controller_plugin import DefaultPermissionsControllerPlugin
from garuda.tests import UnitTestCase

class CustomObject(object):
    """
    """
    def __init__(self, parent_object=None):
        self.id = str(uuid4())
        self.parent_object = parent_object

    def __str__(self):
        """
        """
        return "<CustomObject uuid=%s>" % self.id


class PermissionPluginTestCase(UnitTestCase):
    """
    """
    def __init__(self, name):
        """
        A - B - C - D - E
                    |-  F - G
        """
        super(PermissionPluginTestCase, self).__init__(name)

        self.plugin = DefaultPermissionsControllerPlugin()
        self.user = CustomObject()

        self.objectA = CustomObject()
        self.objectB = CustomObject(parent_object=self.objectA)
        self.objectC = CustomObject(parent_object=self.objectB)
        self.objectD = CustomObject(parent_object=self.objectC)
        self.objectE = CustomObject(parent_object=self.objectD)
        self.objectF = CustomObject(parent_object=self.objectD)
        self.objectG = CustomObject(parent_object=self.objectF)

    def grant_permission(self, to_object, permission):
        """
        """
        self.plugin.create_permission(self.user, to_object, permission)

    def revoke_permission(self, to_object, permission):
        """
        """
        self.plugin.remove_permission(self.user, to_object, permission)

    def _assertHasPermission(self, obj, permission, expected):
        """
        """
        self.assertEquals(self.plugin.has_permission(self.user, obj, permission), expected)

    def assertCanRead(self, obj):
        """
        """
        self._assertHasPermission(obj, 'read', True)

    def assertCanNotRead(self, obj):
        """
        """
        self._assertHasPermission(obj, 'read', False)

    def assertCanUse(self, obj):
        """
        """
        self._assertHasPermission(obj, 'use', True)

    def assertCanNotUse(self, obj):
        """
        """
        self._assertHasPermission(obj, 'use', False)

    def assertCanWrite(self, obj):
        """
        """
        self._assertHasPermission(obj, 'write', True)

    def assertCanNotWrite(self, obj):
        """
        """
        self._assertHasPermission(obj, 'write', False)

    def assertNoSessionExists(self):
        """
        """
        self.assertTrue(self.plugin.is_empty())