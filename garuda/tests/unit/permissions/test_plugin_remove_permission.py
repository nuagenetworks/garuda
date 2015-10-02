# -*- coding: utf-8 -*-

from garuda.tests.unit.permissions import PermissionPluginTestCase


class TestRemovePermissions(PermissionPluginTestCase):
    """
    """

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    def test_remove_read_permission_at_root_level(self):
        """ Remove READ permission at the object level leaves no trace
        """
        self.grant_permission(self.objectA, 'read')
        self.assertCanRead(self.objectA)
        self.revoke_permission(self.objectA, 'read')

        self.assertNoSessionExists()

    def test_remove_write_permission_at_object_level(self):
        """ Remove WRITE permission at the object level leaves no trace
        """
        self.grant_permission(self.objectC, 'write')
        self.revoke_permission(self.objectC, 'write')

        self.assertNoSessionExists()

    def test_remove_multiple_permissions(self):
        """ Remove multiple permission leaves no trace

        """
        self.grant_permission(self.objectC, 'write')
        self.grant_permission(self.objectD, 'use')
        self.grant_permission(self.objectE, 'all')
        self.grant_permission(self.objectF, 'write')

        self.revoke_permission(self.objectD, 'use')
        self.revoke_permission(self.objectC, 'write')
        self.revoke_permission(self.objectF, 'write')
        self.revoke_permission(self.objectE, 'all')

        self.assertNoSessionExists()
