from unittest import TestCase

from garuda.core.plugins import GAAuthenticationPlugin


class TestAuthenticationPlugin(TestCase):
    """
    """
    def test_methods(self):
        """
        """
        plugin = GAAuthenticationPlugin()
        self.assertTrue(plugin.should_manage(request='fake'))

        with self.assertRaises(NotImplementedError):
            self.assertIsNone(plugin.extract_session_identifier(request='fake'))

        with self.assertRaises(NotImplementedError):
            plugin.authenticate(request='request')
