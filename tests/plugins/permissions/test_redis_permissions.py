# -*- coding: utf-8 -*-
from unittest import TestCase

from garuda.plugins.permissions import GARedisPermissionsPlugin

class TestRedisPermissionsPlugin(TestCase):
    """
    """

    def test_identifiers(self):
        """
        """
        auth_plugin = GARedisPermissionsPlugin()
        self.assertEquals(auth_plugin.__class__.manifest().identifier, 'garuda.controller.permissions.redis')
        self.assertEquals(auth_plugin.manifest().identifier, 'garuda.controller.permissions.redis')