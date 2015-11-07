# -*- coding: utf-8 -*-
import redis
from uuid import uuid4
from unittest import TestCase

from garuda.core.controllers import GAPermissionsController
from garuda.core.plugins import GAPermissionsPlugin


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

    def __init__(self):
        """
        """
        self.redis = redis.StrictRedis(host='127.0.0.1', port='6379', db=1)

    @property
    def uuid(self):
        return 'GGGGG-AAAAA-RRRRR-UUUU-DDDDD-AAAA'


class GAPermissionsControllerTestCase(TestCase):
    """
    """

    def __init__(self, name):
        """
        A - B - C - D - E
                    |-  F - G
        """
        super(GAPermissionsControllerTestCase, self).__init__(name)

        self.fake_core_controller = FakeCoreController()
        self.permissions_controller = GAPermissionsController(plugins=[], core_controller=self.fake_core_controller)
        self.permissions_controller.ready()

        self.user = CustomObject()

        self.objectA = CustomObject()
        self.objectB = CustomObject(parent_object=self.objectA)
        self.objectC = CustomObject(parent_object=self.objectB)
        self.objectD = CustomObject(parent_object=self.objectC)
        self.objectE = CustomObject(parent_object=self.objectD)
        self.objectF = CustomObject(parent_object=self.objectD)
        self.objectG = CustomObject(parent_object=self.objectF)

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

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    def test_identifier(self):
        """
        """
        self.assertEquals(self.permissions_controller.identifier(), 'garuda.controller.permissions')
        self.assertEquals(self.permissions_controller.__class__.identifier(), 'garuda.controller.permissions')

    def test_managed_plugin_type(self):
        """
        """
        self.assertEquals(self.permissions_controller.managed_plugin_type(), GAPermissionsPlugin)
        self.assertEquals(self.permissions_controller.__class__.managed_plugin_type(), GAPermissionsPlugin)

    def test_remove_read_permission_at_root_level(self):
        """ Remove READ permission at the object level leaves no trace
        """
        self.permissions_controller.create_permission(self.user, self.objectA, 'read')
        self.assertCanRead(self.objectA)
        self.permissions_controller.remove_permission(self.user, self.objectA, 'read')

        self.assertNoSessionExists()

    def test_remove_write_permission_at_object_level(self):
        """ Remove WRITE permission at the object level leaves no trace
        """
        self.permissions_controller.create_permission(self.user, self.objectC, 'write')
        self.permissions_controller.remove_permission(self.user, self.objectC, 'write')

        self.assertNoSessionExists()

    def test_remove_multiple_permissions(self):
        """ Remove multiple permission leaves no trace

        """
        self.permissions_controller.create_permission(self.user, self.objectC, 'write')
        self.permissions_controller.create_permission(self.user, self.objectD, 'use')
        self.permissions_controller.create_permission(self.user, self.objectE, 'all')
        self.permissions_controller.create_permission(self.user, self.objectF, 'write')

        self.permissions_controller.remove_permission(self.user, self.objectD, 'use')
        self.permissions_controller.remove_permission(self.user, self.objectC, 'write')
        self.permissions_controller.remove_permission(self.user, self.objectF, 'write')
        self.permissions_controller.remove_permission(self.user, self.objectE, 'all')

        self.assertNoSessionExists()

    def test_create_read_permission_at_root_level(self):
        """ Permission READ at the top level should be inherited

        """
        self.permissions_controller.create_permission(self.user, self.objectA, 'read')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanNotUse(self.objectC)
        self.assertCanNotUse(self.objectD)
        self.assertCanNotUse(self.objectE)
        self.assertCanNotUse(self.objectF)
        self.assertCanNotUse(self.objectG)

        self.permissions_controller.remove_permission(self.user, self.objectA, 'read')

    def test_create_read_permission_at_object_level(self):
        """ Permission READ at the top level should be inherited and implicitely extended

        """
        self.permissions_controller.create_permission(self.user, self.objectC, 'read')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanNotUse(self.objectC)
        self.assertCanNotUse(self.objectD)
        self.assertCanNotUse(self.objectE)
        self.assertCanNotUse(self.objectF)
        self.assertCanNotUse(self.objectG)

        self.permissions_controller.remove_permission(self.user, self.objectC, 'read')

    def test_create_use_permission_at_root_level(self):
        """ Permission USE at the top level should be inherited and implicitely extended

        """

        self.permissions_controller.create_permission(self.user, self.objectC, 'use')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanUse(self.objectC)
        self.assertCanUse(self.objectD)
        self.assertCanUse(self.objectE)
        self.assertCanUse(self.objectF)
        self.assertCanUse(self.objectG)

        # Write
        self.assertCanNotWrite(self.objectA)
        self.assertCanNotWrite(self.objectB)
        self.assertCanNotWrite(self.objectC)
        self.assertCanNotWrite(self.objectD)
        self.assertCanNotWrite(self.objectE)
        self.assertCanNotWrite(self.objectF)
        self.assertCanNotWrite(self.objectG)

        self.permissions_controller.remove_permission(self.user, self.objectC, 'use')

    def test_override_write_permission_before_object(self):
        """ Permission WRITE before an existing USE permission should override it
        """
        self.permissions_controller.create_permission(self.user, self.objectC, 'use')
        self.permissions_controller.create_permission(self.user, self.objectB, 'write')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanUse(self.objectB)
        self.assertCanUse(self.objectC)
        self.assertCanUse(self.objectD)
        self.assertCanUse(self.objectE)
        self.assertCanUse(self.objectF)
        self.assertCanUse(self.objectG)

        # Write
        self.assertCanNotWrite(self.objectA)
        self.assertCanWrite(self.objectB)
        self.assertCanWrite(self.objectC)
        self.assertCanWrite(self.objectD)
        self.assertCanWrite(self.objectE)
        self.assertCanWrite(self.objectF)
        self.assertCanWrite(self.objectG)

        self.permissions_controller.remove_permission(self.user, self.objectB, 'write')
        self.permissions_controller.remove_permission(self.user, self.objectC, 'use')

    def test_override_write_permission_after_object(self):
        """ Permission WRITE after an existing USE permission should override it
        """
        self.permissions_controller.create_permission(self.user, self.objectC, 'use')
        self.permissions_controller.create_permission(self.user, self.objectF, 'write')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanUse(self.objectC)
        self.assertCanUse(self.objectD)
        self.assertCanUse(self.objectE)
        self.assertCanUse(self.objectF)
        self.assertCanUse(self.objectG)

        # Write
        self.assertCanNotWrite(self.objectA)
        self.assertCanNotWrite(self.objectB)
        self.assertCanNotWrite(self.objectC)
        self.assertCanNotWrite(self.objectD)
        self.assertCanNotWrite(self.objectE)
        self.assertCanWrite(self.objectF)
        self.assertCanWrite(self.objectG)

        self.permissions_controller.remove_permission(self.user, self.objectF, 'write')
        self.permissions_controller.remove_permission(self.user, self.objectC, 'use')

    def test_create_same_permission_twice(self):
        """
        """
        self.permissions_controller.create_permission(self.user, self.objectA, 'read')
        self.permissions_controller.create_permission(self.user, self.objectA, 'read')

        self.assertCanRead(self.objectA)

        self.permissions_controller.remove_permission(self.user, self.objectA, 'read')

        self.assertCanNotRead(self.objectA)
