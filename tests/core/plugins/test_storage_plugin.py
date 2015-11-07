from unittest import TestCase

from garuda.core.plugins import GAStoragePlugin


class TestStoragePlugin(TestCase):
    """
    """
    def test_methods(self):
        """
        """
        plugin = GAStoragePlugin()
        self.assertTrue(plugin.should_manage(resource_name='fake', identifier='fake'))

    def test_instantiate_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.instantiate(resource_name='fake')

    def test_count_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.count(parent='fake', resource_name='fake', filter='fake')

    def test_get_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.get(resource_name='fake', identifier='fake', filter='fake')

    def test_get_all_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.get_all(parent='fake', resource_name='fake', page=1, page_size=1, filter='fake', order_by='fake')

    def test_create_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.create(resource='fake', parent='fake', user_identifier='fake')

    def test_update_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.update(resource='fake', user_identifier='fake')

    def test_delete_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.delete(resource='fake', cascade=True, user_identifier='fake')

    def test_delete_multiple_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.delete_multiple(resources=['fake'], cascade=True, user_identifier='fake')

    def test_assign_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.assign(resource_name='fake', resources=['fake'], parent='fake', user_identifier='fake')
