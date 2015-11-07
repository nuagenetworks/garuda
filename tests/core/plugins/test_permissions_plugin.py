from unittest import TestCase

from garuda.core.plugins import GAPermissionsPlugin


class TestPermissionsPlugin(TestCase):
    """
    """
    def test_methods(self):
        """
        """
        plugin = GAPermissionsPlugin()
        self.assertTrue(plugin.should_manage(resource_name='fake', identifier='fake'))

    def test_auth_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.interpret_permissions()
