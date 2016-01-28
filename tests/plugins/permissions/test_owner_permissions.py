# -*- coding: utf-8 -*-
from unittest import TestCase

from garuda.core.lib import GASDKLibrary
from garuda.plugins.permissions import GAOwnerPermissionsPlugin

import tests.tstdk.v1_0 as tstdk



class TestOwnerPermissionsPlugin(TestCase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)
        cls.auth_plugin = GAOwnerPermissionsPlugin()

    def test_should_manage(self):
        """
        """
        self.assertEquals(self.auth_plugin.should_manage(), True)

    def test_identifiers(self):
        """
        """
        self.assertEquals(self.auth_plugin.__class__.manifest().identifier, 'garuda.controller.permissions.owner')
        self.assertEquals(self.auth_plugin.manifest().identifier, 'garuda.controller.permissions.owner')

    def test_has_permission(self):
        """
        """
        enterprise = tstdk.GAEnterprise(owner='me')
        self.assertEquals(self.auth_plugin.has_permission(resource='me', target=enterprise, permission='fake', explicit_only=False), True)
        self.assertEquals(self.auth_plugin.has_permission(resource='not_me', target=enterprise, permission='fake', explicit_only=False), False)

    def test_child_ids_with_permission(self):
        """
        """
        enterprise = tstdk.GAEnterprise(owner='me')
        self.assertEquals(self.auth_plugin.child_ids_with_permission(resource='fake', parent='fake', children_type='fake', permission='fake'), '__OWNER_ONLY__')

    def test_is_empty(self):
        """
        """
        self.assertEquals(self.auth_plugin.is_empty(), False)