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

    def test_create_permission_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.create_permission(resource='fake', target='fake', permission='fake', explicit=True, parent_permission_id='fake')

    def test_remove_permission_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.remove_permission(resource='fake', target='fake', permission='fake')

    def test_remove_all_permissions_of_resource_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.remove_all_permissions_of_resource(resource='fake')

    def test_remove_all_permissions_for_target_ids_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.remove_all_permissions_for_target_ids(target_ids='fake')

    def test_has_permission_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.has_permission(resource='fake', target='fake', permission='fake', explicit_only=False)

    def test_child_ids_with_permission_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.child_ids_with_permission(resource='fake', parent=None, children_type='fake', permission='fake')

    def test_is_empty_required(self):
        """
        """
        plugin = GAPermissionsPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.is_empty()
