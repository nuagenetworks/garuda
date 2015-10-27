# -*- coding:utf-8 -*-

import redis
from uuid import uuid4

from garuda.core.controllers import GAPermissionsController
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


class FakeCoreController(object):

    @property
    def uuid(self):
        return 'GGGGG-AAAAA-RRRRR-UUUU-DDDDD-AAAA'

class PermissionsControllerTestCase(UnitTestCase):
    """
    """
    def __init__(self, name):
        """
        A - B - C - D - E
                    |-  F - G
        """
        super(PermissionsControllerTestCase, self).__init__(name)

        redis_connection            = redis.StrictRedis(host='127.0.0.1', port='6379', db=0)
        self.fake_core_controller   = FakeCoreController()
        self.permissions_controller = GAPermissionsController(plugins=[], core_controller=self.fake_core_controller, redis_conn=redis_connection)
        self.permissions_controller.ready()

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
        self.permissions_controller.create_permission(self.user, to_object, permission)

    def revoke_permission(self, to_object, permission):
        """
        """
        self.permissions_controller.remove_permission(self.user, to_object, permission)

    def _assertHasPermission(self, obj, permission, expected):
        """
        """
        self.assertEquals(self.permissions_controller.has_permission(self.user, obj, permission), expected)

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
        self.assertTrue(self.permissions_controller.is_empty())