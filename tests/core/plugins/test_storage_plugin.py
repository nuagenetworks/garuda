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
            plugin.count(user_identifier='owner_identifier', parent='fake', resource_name='fake', filter='fake')

    def test_get_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.get(user_identifier='owner_identifier', resource_name='fake', identifier='fake', filter='fake')

    def test_get_all_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.get_all(user_identifier='owner_identifier', parent='fake', resource_name='fake', page=1, page_size=1, filter='fake', order_by='fake')

    def test_create_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.create(user_identifier='owner_identifier', resource='fake', parent='fake')

    def test_update_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.update(user_identifier='owner_identifier', resource='fake')

    def test_delete_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.delete(user_identifier='owner_identifier', resource='fake', cascade=True)

    def test_delete_multiple_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.delete_multiple(user_identifier='owner_identifier', resources=['fake'], cascade=True)

    def test_assign_required(self):
        """
        """
        plugin = GAStoragePlugin()
        with self.assertRaises(NotImplementedError):
            plugin.assign(user_identifier='owner_identifier', resource_name='fake', resources=['fake'], parent='fake')
