from unittest import TestCase

from garuda.core.models import GAPlugin


class TestPlugin(TestCase):
    """
    """
    def test_methods(self):
        """
        """
        plugin = GAPlugin()
        self.assertIsNone(plugin.will_register())
        self.assertIsNone(plugin.did_register())
        self.assertIsNone(plugin.will_unregister())
        self.assertIsNone(plugin.did_unregister())

    def test_manifest_required(self):
        """
        """
        plugin = GAPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.manifest()

        with self.assertRaises(NotImplementedError):
            plugin.__class__.manifest()
